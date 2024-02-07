from typing import Optional

from openai.types.chat.chat_completion import ChatCompletion

from data_assessment_agent.config.toml_support import prompts
from data_assessment_agent.service.openai_support import (
    create_completion,
    extract_function_call_arguments,
)
from data_assessment_agent.model.yes_no_question import question_type_spec


async def is_yes_no_question(question: str) -> bool:
    user_message = create_user_message(question)
    system_message = prompts["question_type"]["system_message"]
    completion = await create_completion(
        system_message, user_message, question_type_spec
    )
    return extract_from(completion)


def extract_from(
    chat_completion: Optional[ChatCompletion], key="is_yes_no_question"
) -> bool:
    arguments = extract_function_call_arguments(chat_completion)
    if key in arguments:
        return arguments[key]
    return False


def create_user_message(question: str) -> str:
    user_prompt = prompts["question_type"]["user_message"]
    return user_prompt.format(question=question)


if __name__ == "__main__":
    import asyncio

    response = asyncio.run(is_yes_no_question("Do you have a clearly defined business strategy?"))
    assert response is True

    response = asyncio.run(is_yes_no_question("Which kind of data are you processing in your company?"))
    assert response is False



