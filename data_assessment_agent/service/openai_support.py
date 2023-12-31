import json
from typing import Optional, List

from data_assessment_agent.config.log_factory import logger
from data_assessment_agent.config.config import cfg

from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_message import FunctionCall


async def create_completion(
    system_message: str, user_message: str, function_spec: dict
) -> ChatCompletion:
    logger.info("completion user message: %s", user_message)
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


def extract_function_call_arguments(chat_completion: Optional[ChatCompletion]) -> dict:
    choices = chat_completion.choices
    if len(choices) > 0:
        message = choices[0].message
        function_call: Optional[FunctionCall] = message.function_call
        if function_call is not None:
            return json.loads(function_call.arguments)
    return {}
