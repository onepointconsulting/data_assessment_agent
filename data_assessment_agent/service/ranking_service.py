import json
from typing import Optional, List

from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_message import FunctionCall

from data_assessment_agent.config.log_factory import logger
from data_assessment_agent.config.toml_support import prompts
from data_assessment_agent.config.config import cfg
from data_assessment_agent.model.ranking import (
    question_ranking_spec,
    topic_ranking_spec,
)


async def create_completion(
    system_message: str, user_message: str, function_spec: dict
) -> ChatCompletion:
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]
    kwargs = {"function_call": "auto"}
    completion = await cfg.open_ai_client.chat.completions.create(
        model=cfg.openai_model,
        temperature=cfg.open_ai_temperature,
        messages=messages,
        functions=[function_spec],
        stream=False,
        **kwargs,
    )
    return completion


async def rank_questions(
    topic: str, question_answers: str, ranking_questions: str
) -> List[str]:
    logger.info("Ranking questions")
    user_message = create_user_message(topic, question_answers, ranking_questions)
    system_message = prompts["ranking"]["system_message"]
    completion = await create_completion(
        system_message, user_message, question_ranking_spec
    )
    return extract_ranking(completion)


def extract_ranking(
    chat_completion: Optional[ChatCompletion], ranking_key="ranked_questions"
) -> List[str]:
    choices = chat_completion.choices
    if len(choices) > 0:
        message = choices[0].message
        function_call: Optional[FunctionCall] = message.function_call
        if function_call is not None:
            arguments = json.loads(function_call.arguments)
            ranked_questions_key = ranking_key
            if ranked_questions_key in arguments:
                return arguments[ranked_questions_key]
    return []


def create_user_message(
    topic: str, question_answers: str, ranking_questions: str
) -> str:
    user_prompt = prompts["ranking"]["user_message"]
    return user_prompt.format(
        topic=topic,
        question_answers=question_answers,
        ranking_questions=ranking_questions,
    )


async def rank_topics(question_answers: str, ranking_topics_str: str) -> List[str]:
    logger.info("Ranking topics")
    user_message = create_topics_user_message(question_answers, ranking_topics_str)
    system_message = prompts["ranking"]["topics"]["system_message"]
    completion = await create_completion(
        system_message, user_message, topic_ranking_spec
    )
    return extract_ranking(completion, ranking_key="ranked_topics")


def create_topics_user_message(question_answers: str, ranking_topics_str: str) -> str:
    user_prompt = prompts["ranking"]["topics"]["user_message"]
    return user_prompt.format(
        question_answers=question_answers, ranking_topics=ranking_topics_str
    )


if __name__ == "__main__":
    import asyncio
    from data_assessment_agent.test.provider.ranking_prompt_provider import (
        ranking_prompt_provider,
        topics_ranking_prompt_provider,
    )

    def test_question_ranking():
        topic, question_answers, ranking_questions = ranking_prompt_provider()
        ranked_questions = asyncio.run(
            rank_questions(topic, question_answers, ranking_questions)
        )
        for i, question in enumerate(ranked_questions):
            print(i, question)

    question_answers, ranking_topics_str = topics_ranking_prompt_provider()
    ranked_topics = asyncio.run(rank_topics(question_answers, ranking_topics_str))
    for i, topic in enumerate(ranked_topics):
        print(i, topic)
