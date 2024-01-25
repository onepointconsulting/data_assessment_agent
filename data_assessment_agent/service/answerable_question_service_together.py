import json

from data_assessment_agent.config.log_factory import logger
from data_assessment_agent.config.config import cfg
from data_assessment_agent.config.toml_support import prompts
from data_assessment_agent.model.db_model import Question

from data_assessment_agent.utils.together_support import execute_together_request


def create_user_message(question_obj: Question) -> str:
    prompt_template = prompts["unanswerable"]["user_message"]
    return prompt_template.format(
        topic=question_obj.topic.name, question=question_obj.question
    )


def extract_bool(text: str):
    try:
        parsed_dict = json.loads(text)
        res = False
        if "output" in parsed_dict:
            output = parsed_dict["output"]
            if "choices" in output:
                choices = output["choices"]
                for choice in choices:
                    if "text" in choice:
                        logger.info("Trying to parse: %s", choice["text"])
                        return "yes" in choice["text"].lower()
        return res
    except:
        logger.exception("Could not determine whether question is answerable or not")
        logger.error(text)
    return False


async def answerable_question(question_obj: Question) -> bool:
    prompt = create_user_message(question_obj)
    return await execute_together_request(
        prompt,
        extract_bool,
        cfg.together_model_alt_prompt_template,
        cfg.together_model_alt_stop,
        cfg.together_model_alt,
        False,
    )
