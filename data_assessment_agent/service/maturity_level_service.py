from typing import Union
from collections import defaultdict
from pathlib import Path

import numpy as np
from openai.types.chat.chat_completion import ChatCompletion
from jinja2 import FileSystemLoader, Environment

from data_assessment_agent.config.log_factory import logger
from data_assessment_agent.config.toml_support import prompts
from data_assessment_agent.service.openai_support import create_completion
from data_assessment_agent.model.maturity_level import (
    MaturityLevelResponse,
    ScoredMaturityLevelResponse,
    maturity_level_spec,
    MATURITY_LEVEL_DICT,
    MATURITY_LEVEL_DICT_INVERTED,
)
from data_assessment_agent.model.maturity_level import MaturityLevelEnum
from data_assessment_agent.service.persistence_service_async import (
    insert_report,
    select_report,
    select_session_report,
)
from data_assessment_agent.config.config import cfg
from data_assessment_agent.service.report_helper import generate_report_date


async def generate_session_report_text(session_id: str) -> str:
    sessions = await select_session_report(session_id)
    str = ""
    topic_scores = defaultdict(int)
    topic_scores_max = defaultdict(int)
    current_topic = ""

    def generate_topic_score(current_topic: str):
        return f"""
Topic '{current_topic}' score: {topic_scores[current_topic]} out of {topic_scores_max[current_topic]}
Percentage: {topic_scores[current_topic] / topic_scores_max[current_topic] * 100}% 
"""

    for session in sessions:
        question, answer, topic, score, max_score = (
            session.question,
            session.answer,
            session.topic,
            session.score,
            session.max_score,
        )
        topic_scores[topic] += score
        topic_scores_max[topic] += max_score
        topic_change = current_topic != topic
        if topic_change:
            if len(current_topic) > 0:
                str += generate_topic_score(current_topic)
            current_topic = topic
            str += f"""
# Category: {topic}
"""
        str += f"""
Question: {question}
Answer: {answer}
Score: {score}
"""

    if len(current_topic) > 0:
        str += generate_topic_score(current_topic)

    return str


async def create_maturity_report_for_session(
    session_id: str,
) -> Union[ScoredMaturityLevelResponse, None]:
    report = await select_report(session_id)
    if report is None:
        report_text = await generate_session_report_text(session_id)
        maturity_level_report = await create_maturity_report(report_text)
        await insert_report(session_id, maturity_level_report)
        return maturity_level_report
    else:
        return ScoredMaturityLevelResponse.model_validate_json(report)


async def generate_maturity_level_report(session_id: str) -> Union[Path, None]:
    template_loader = FileSystemLoader(cfg.templates_folder)
    template_env = Environment(loader=template_loader, enable_async=True)
    template = template_env.get_template("maturity-assessment.html")
    context = await create_maturity_level_report_context(session_id)
    results_template = await template.render_async(context)
    report_path: Path = cfg.report_tmp_path / f"maturity-assessmen_{session_id}.html"
    report_path.write_text(results_template, encoding="utf-8")
    return report_path


async def create_maturity_level_report_context(session_id: str) -> dict:
    scored_maturity_level_report = await create_maturity_report_for_session(session_id)
    return {
        "score": f"{scored_maturity_level_report.score:.2f}",
        "maturity_level": scored_maturity_level_report.maturity_level.name,
        "maturity_level_overall_evaluation": scored_maturity_level_report.overall_evaluation,
        "maturity_levels": scored_maturity_level_report.maturity_levels,
        "timestamp": generate_report_date(),
        "maturity_level_enum": MaturityLevelEnum,
    }


async def create_maturity_report(
    report: str,
) -> Union[ScoredMaturityLevelResponse, None]:
    logger.info("Create maturity report")
    user_message = create_user_message(report)
    system_message = prompts["report"]["system_message"]
    completion = await create_completion(
        system_message, user_message, maturity_level_spec
    )
    maturity_level_response = extract_maturity_levels(completion)
    if not maturity_level_response:
        return None
    return calculate_overall_score(maturity_level_response)


def create_user_message(report: str) -> str:
    user_message_template = prompts["report"]["user_message"]
    return user_message_template.format(report=report)


def extract_maturity_levels(
    completion: ChatCompletion,
) -> Union[MaturityLevelResponse, None]:
    if len(completion.choices) < 1:
        return None
    return MaturityLevelResponse.model_validate_json(
        completion.choices[0].message.function_call.arguments
    )


def calculate_overall_score(
    maturity_level_response: MaturityLevelResponse,
) -> ScoredMaturityLevelResponse:
    scores = [
        MATURITY_LEVEL_DICT[ml.maturity_level]
        for ml in maturity_level_response.maturity_levels
    ]
    score = np.mean(scores).item()
    maturity_level = MATURITY_LEVEL_DICT_INVERTED[round(score)]
    return ScoredMaturityLevelResponse(
        score=score,
        maturity_level=maturity_level,
        maturity_levels=maturity_level_response.maturity_levels,
        overall_evaluation=maturity_level_response.overall_evaluation,
    )


if __name__ == "__main__":
    from data_assessment_agent.test.provider.maturity_level_provider import (
        provide_session_report,
    )
    import asyncio

    def generate_session_report_text_execute():
        session_id = "da437e34-e64f-45a6-9042-36808d8fc8ea"
        text = asyncio.run(generate_session_report_text(session_id))
        target_file = Path("./docs/session_output.txt")
        target_file.write_text(text, encoding="utf-8")

    def generate_maturity_test():
        report = provide_session_report()
        maturity_response = asyncio.run(create_maturity_report(report))
        assert maturity_response is not None
        for maturity_level in maturity_response.maturity_levels:
            print("#", maturity_level.category)
            print("Level:", maturity_level.maturity_level)
            print("Reasoning:", maturity_level.reasoning)
            print("Missing info:", maturity_level.missing_information_comments)

            print()
        print(
            "Overall score: **",
            maturity_response.score,
            f"out of {MATURITY_LEVEL_DICT[MaturityLevelEnum.OPTIMIZED]} **",
        )
        print("Overall maturity: **", maturity_response.maturity_level, " **")
        print(maturity_response.model_dump_json())

    def generate_maturity_level_report_test():
        session_id = "da437e34-e64f-45a6-9042-36808d8fc8ea"
        maturity_level_path = asyncio.run(generate_maturity_level_report(session_id))
        assert maturity_level_path is not None
        print(maturity_level_path)

    generate_maturity_level_report_test()
