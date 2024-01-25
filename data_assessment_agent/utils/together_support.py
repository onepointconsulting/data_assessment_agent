from typing import List, Callable, Any
import json

import aiohttp

from data_assessment_agent.config.log_factory import logger
from data_assessment_agent.config.config import cfg
from data_assessment_agent.utils.date_utils import generate_ISO_8601_timestamp

endpoint = "https://api.together.xyz/inference"


def generate_json(
    prompt: str,
    prompt_template: str = "[INST]{prompt}[/INST]",
    stop_list: List[str] = ["[/INST]", "</s>"],
    model: str = cfg.together_model,
) -> dict:
    return {
        "model": model,
        "max_tokens": cfg.together_max_tokens,
        "prompt": prompt_template.format(prompt=prompt),
        "request_type": "language-model-inference",
        "temperature": cfg.together_temperature,
        "top_p": cfg.together_top_p,
        "top_k": cfg.together_top_k,
        "stop": stop_list,
        "negative_prompt": "",
        "repetitive_penalty": 1,
        "update_at": generate_ISO_8601_timestamp(),
    }


def generate_headers() -> dict:
    return {
        "Authorization": f"Bearer {cfg.together_api_key}",
        "Content-Type": "application/json",
    }


async def execute_together_request(
    prompt: str,
    text_extraction_func: Callable,
    prompt_template: str = "[INST]{prompt}[/INST]",
    stop_list: List[str] = ["[/INST]", "</s>"],
    model: str = cfg.together_model,
    error_return: Any = [],
) -> List[str]:
    async with aiohttp.ClientSession() as session:
        data = generate_json(prompt, prompt_template, stop_list, model)
        logger.info(data)
        async with session.post(
            endpoint, data=json.dumps(data), headers=generate_headers()
        ) as res:
            if res.status >= 200 and res.status < 300:
                text = await res.text()
                return text_extraction_func(text)
            logger.error(
                "Failed to rank with togetheer AI. Status code: %d", res.status
            )
            return error_return
