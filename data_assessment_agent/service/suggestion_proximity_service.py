from typing import List, Optional

from openai.types.chat.chat_completion import ChatCompletion

from data_assessment_agent.config.log_factory import logger
from data_assessment_agent.config.toml_support import prompts
from data_assessment_agent.model.suggestions import closest_suggestion_spec
from data_assessment_agent.service.openai_support import (
    create_completion,
    extract_function_call_arguments,
)

PROMPT_KEY = "suggestion_proximity"


def create_user_message(answer: str, suggestions: List[str]) -> str:
    user_prompt = prompts[PROMPT_KEY]["user_message"]
    return user_prompt.format(answer=answer, suggestions="\n".join(suggestions))


async def rank_suggestions(answer: str, suggestions: List[str]) -> Optional[str]:
    logger.info("Ranking questions")
    user_message = create_user_message(answer, suggestions)
    system_message = prompts[PROMPT_KEY]["system_message"]
    completion = await create_completion(
        system_message, user_message, closest_suggestion_spec
    )
    return extract_closest_suggestion(completion)


def extract_closest_suggestion(
    chat_completion: Optional[ChatCompletion], key="suggestion"
) -> Optional[str]:
    arguments = extract_function_call_arguments(chat_completion)
    if key in arguments:
        return arguments[key]
    return None


if __name__ == "__main__":
    import asyncio
    from data_assessment_agent.test.provider.suggestion_provider import (
        create_multiple_suggestions,
    )

    answer, suggestions = create_multiple_suggestions()
    res = asyncio.run(rank_suggestions(answer, suggestions))
    assert res is not None
    print(res)
