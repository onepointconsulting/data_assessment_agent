import sys
import asyncio

from data_assessment_agent.config.log_factory import logger
from data_assessment_agent.service.persistence_service import (
    load_questions,
    save_suggested_response,
    suggestion_exists_for,
)
from data_assessment_agent.model.db_model import Question
from data_assessment_agent.service.suggestion_service import generate_suggestions
from data_assessment_agent.model.db_model import create_db_suggested_response
from data_assessment_agent.service.suggestion_service import (
    PROMPT_CATEGORY_YES_NO,
    PROMPT_CATEGORY_OPEN_ENDED,
)


def generate_suggestion(
    question_counter: int, counter: int, question_obj: Question, prompt_category
) -> int:
    try:
        suggested_response_list = asyncio.run(
            generate_suggestions(
                question_obj.question, question_obj.topic.name, prompt_category
            )
        )
        for resp in suggested_response_list.suggested_responses:
            db_suggested_response = create_db_suggested_response(resp, question_obj)
            saved_suggestion = save_suggested_response(db_suggested_response)
            logger.info("Saved %s", saved_suggestion)
            counter += 1
        logger.info(
            "Generated %d suggestions for %d questions",
            counter,
            question_counter,
        )
        return counter
    except:
        logger.exception("Could not save suggestions for %s", question_obj)


if __name__ == "__main__":
    logger.info("Clearing suggested responses")
    # clear_suggested_responses()
    logger.info("Getting all questions")
    questions = load_questions()
    question_counter = 0
    counter = 0

    is_yes_no = True
    if len(sys.argv) > 1 and sys.argv[1] == "open_ended":
        is_yes_no = False

    for question_obj in questions:
        if question_obj.yes_no_question:
            if is_yes_no and not suggestion_exists_for(question_obj):
                question_counter += 1
                counter += generate_suggestion(
                    question_counter, counter, question_obj, PROMPT_CATEGORY_YES_NO
                )
        else:
            if is_yes_no == False and not suggestion_exists_for(question_obj):
                question_counter += 1
                counter += generate_suggestion(
                    question_counter, counter, question_obj, PROMPT_CATEGORY_OPEN_ENDED
                )
