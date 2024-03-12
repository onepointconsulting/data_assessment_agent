from typing import Callable

from data_assessment_agent.config.log_factory import logger
from data_assessment_agent.config.toml_support import prompts
from data_assessment_agent.config.config import cfg


CLARIFICATION_KEY = "clarification"


def create_user_message(question: str, topic: str) -> str:
    user_prompt = prompts[CLARIFICATION_KEY]["user_message"]
    return user_prompt.format(question=question, topic=topic)


async def stream_clarification(question: str, topic: str, stream_func: Callable):
    logger.info("Getting clarification for %s", question)
    user_message = create_user_message(question, topic)
    system_message = prompts[CLARIFICATION_KEY]["system_message"]
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]
    completion = await cfg.open_ai_client.chat.completions.create(
        model=cfg.openai_model,
        temperature=cfg.open_ai_temperature,
        messages=messages,
        stream=True,
    )
    async for chunk in completion:
        chunk_message = chunk.choices[0].delta  # extract the message
        if chunk_message.content is not None:
            message_text = chunk_message.content
            await stream_func(message_text)


if __name__ == "__main__":
    import asyncio
    from data_assessment_agent.test.provider.clarification_provider import (
        clarification_data_1,
    )

    question, topic = clarification_data_1()

    asyncio.run(
        stream_clarification(question, topic, lambda x: print(x, end="", flush=True))
    )
