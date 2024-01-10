import requests
import json
from typing import List

from data_assessment_agent.config.toml_support import prompts
from data_assessment_agent.config.config import cfg
from data_assessment_agent.config.log_factory import logger
from data_assessment_agent.utils.date_utils import generate_ISO_8601_timestamp


def create_user_message(
    topic: str, question_answers: str, ranking_questions: str
) -> str:
    user_prompt = prompts["ranking"]["together"]["user_message"]
    return user_prompt.format(
        topic=topic,
        question_answers=question_answers,
        ranking_questions=ranking_questions,
    )


def rank_questions_request(prompt: str) -> List[str]:
    logger.info("Ranking prompt: \n%s", prompt)
    endpoint = "https://api.together.xyz/inference"
    res = requests.post(
        endpoint,
        json={
            "model": cfg.together_model,
            "max_tokens": cfg.together_max_tokens,
            "prompt": f"[INST]{prompt}[/INST]",
            "request_type": "language-model-inference",
            "temperature": cfg.together_temperature,
            "top_p": cfg.together_top_p,
            "top_k": cfg.together_top_k,
            "stop": ["[/INST]", "</s>"],
            "negative_prompt": "",
            "repetitive_penalty": 1,
            "update_at": generate_ISO_8601_timestamp(),
        },
        headers={
            "Authorization": f"Bearer {cfg.together_api_key}",
        },
    )
    text = res.text
    parsed_dict = json.loads(text)
    res = []
    try:
        if "output" in parsed_dict:
            output = parsed_dict["output"]
            if "choices" in output:
                choices = output["choices"]
                for choice in choices:
                    if "text" in choice:
                        ranked = json.loads(choice["text"])
                        for q in ranked:
                            res.append(q)
    except:
        logger.exception("Could not rank files with togetherai")
        logger.error(text)
    return res


async def rank_questions_together(
    topic: str, question_answers: str, ranking_questions: str
) -> List[str]:
    prompt = create_user_message(topic, question_answers, ranking_questions)
    return rank_questions_request(prompt)