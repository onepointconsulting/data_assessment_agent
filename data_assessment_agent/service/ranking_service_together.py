import requests
import json
from typing import List
import aiohttp

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


endpoint = "https://api.together.xyz/inference"


def generate_json(prompt: str) -> dict:
    return {
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
    }


def generate_headers() -> dict:
    return {
        "Authorization": f"Bearer {cfg.together_api_key}",
        "Content-Type": "application/json"
    }


async def arank_questions_request(prompt: str) -> List[str]:
    async with aiohttp.ClientSession() as session:
        data = generate_json(prompt)
        logger.info(data)
        async with session.post(endpoint, data=json.dumps(data), headers=generate_headers()) as res:
            if res.status >= 200 and res.status < 300:
                text = await res.text()
                return extract_ranking(text)
            logger.error("Failed to rank with togetheer AI. Status code: %d", res.status)
            return []


def rank_questions_request(prompt: str) -> List[str]:
    logger.info("Ranking prompt: \n%s", prompt)

    res = requests.post(
        endpoint,
        json=generate_json(prompt),
        headers=generate_headers(),
    )
    text = res.text
    return extract_ranking(text)


def extract_ranking(text: str):
    try:
        parsed_dict = json.loads(text)
        res = []
        if "output" in parsed_dict:
            output = parsed_dict["output"]
            if "choices" in output:
                choices = output["choices"]
                for choice in choices:
                    if "text" in choice:
                        logger.info("Trying to parse: %s", choice["text"])
                        ranked = json.loads(choice["text"])
                        for q in ranked:
                            res.append(q)
        return res
    except:
        logger.exception("Could not rank files with togetherai")
        logger.error(text)
    return []


async def rank_questions_together(
    topic: str, question_answers: str, ranking_questions: str
) -> List[str]:
    prompt = create_user_message(topic, question_answers, ranking_questions)
    return await arank_questions_request(prompt)


if __name__ == "__main__":
    from data_assessment_agent.test.provider.topic_provider import create_topic_title
    from data_assessment_agent.test.provider.question_provider import (
        create_question_answers,
        create_ranking_questions,
    )
    import asyncio

    question_answers = create_question_answers()
    topic = create_topic_title()
    ranking_questions = create_ranking_questions()
    ranked_questions = asyncio.run(rank_questions_together(topic, question_answers, ranking_questions))
    for q in ranked_questions:
        print(q)
