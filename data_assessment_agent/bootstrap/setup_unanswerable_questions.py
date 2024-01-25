import time
import asyncio

from data_assessment_agent.config.log_factory import logger
from data_assessment_agent.service.persistence_service import load_questions
from data_assessment_agent.service.persistence_service_async import (
    update_yes_no_question,
)
from data_assessment_agent.config.toml_support import prompts
from data_assessment_agent.service.answerable_question_service_together import (
    create_user_message,
    answerable_question,
)


if __name__ == "__main__":
    logger.info("Clearing suggested responses")
    logger.info("Getting all questions")
    questions = load_questions()
    prompt_template = prompts["unanswerable"]["user_message"]
    for question_obj in questions:
        prompt = create_user_message(question_obj)
        answerable = asyncio.run(answerable_question(question_obj))
        print("======================")
        print(question_obj.question)
        print(f"answerable: {answerable}")
        print("======================")
        question_obj.yes_no_question = answerable
        asyncio.run(update_yes_no_question(question_obj))
        time.sleep(1.0)
