import json
from typing import Optional, List

from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_message import FunctionCall

from data_assessment_agent.config.toml_support import prompts
from data_assessment_agent.config.config import cfg
from data_assessment_agent.model.ranking import question_ranking_spec


async def rank_questions(
    topic: str, question_answers: str, ranking_questions: str
) -> List[str]:
    user_message = create_user_message(topic, question_answers, ranking_questions)
    system_message = prompts["ranking"]["system_message"]
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]
    kwargs = {"function_call": "auto"}
    completion = await cfg.open_ai_client.chat.completions.create(
        model=cfg.openai_model,
        temperature=cfg.open_ai_temperature,
        messages=messages,
        functions=[question_ranking_spec],
        stream=False,
        **kwargs,
    )
    return extract_ranking(completion)


def extract_ranking(chat_completion: Optional[ChatCompletion]) -> List[str]:
    choices = chat_completion.choices
    if len(choices) > 0:
        message = choices[0].message
        function_call: Optional[FunctionCall] = message.function_call
        if function_call is not None:
            arguments = json.loads(function_call.arguments)
            ranked_questions_key = "ranked_questions"
            if ranked_questions_key in arguments:
                return arguments[ranked_questions_key]
    return []


def create_user_message(
    topic: str, question_answers: str, ranking_questions: str
) -> str:
    user_prompt = prompts["ranking"]["user_message"]
    user_message = user_prompt.format(
        topic=topic,
        question_answers=question_answers,
        ranking_questions=ranking_questions,
    )
    return user_message


if __name__ == "__main__":
    import asyncio
    from data_assessment_agent.test.provider.ranking_prompt_provider import (
        ranking_prompt_provider,
    )

    topic, question_answers, ranking_questions = ranking_prompt_provider()
    ranked_questions = asyncio.run(
        rank_questions(topic, question_answers, ranking_questions)
    )
    for i, question in enumerate(ranked_questions):
        print(i, question)
