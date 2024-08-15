from typing import Union

import numpy as np
from openai.types.chat.chat_completion import ChatCompletion

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
    )


if __name__ == "__main__":
    from data_assessment_agent.test.provider.maturity_level_provider import (
        provide_session_report,
    )
    from data_assessment_agent.model.maturity_level import MaturityLevelEnum
    import asyncio

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
