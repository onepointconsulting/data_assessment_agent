import time
import asyncio

from data_assessment_agent.config.log_factory import logger
from data_assessment_agent.service.persistence_service import load_questions
from data_assessment_agent.service.persistence_service_async import (
    update_yes_no_question,
)


from data_assessment_agent.service.yes_no_question_service_openai import (
    is_yes_no_question,
)


if __name__ == "__main__":
    logger.info("Clearing suggested responses")
    logger.info("Getting all questions")
    questions = load_questions()
    for question_obj in questions:
        try:
            print("======================")
            print(question_obj.question)
            question_obj.yes_no_question = asyncio.run(
                is_yes_no_question(question_obj.question)
            )
            print(f"answerable: {question_obj.yes_no_question}")
            print("======================")
            asyncio.run(update_yes_no_question(question_obj))
            time.sleep(1.0)
        except:
            logger.exception(f"Cannot process question {question_obj.question}")
