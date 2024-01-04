import asyncio

from data_assessment_agent.config.log_factory import logger
from data_assessment_agent.service.persistence_service import (
    load_questions,
    save_suggested_response,
    suggestion_exists_for,
)
from data_assessment_agent.service.suggestion_service import generate_suggestions
from data_assessment_agent.model.db_model import create_db_suggested_response


if __name__ == "__main__":
    logger.info("Clearing suggested responses")
    # clear_suggested_responses()
    logger.info("Getting all questions")
    questions = load_questions()
    for question_obj in questions:
        if not suggestion_exists_for(question_obj):
            try:
                suggested_response_list = asyncio.run(
                    generate_suggestions(question_obj.question, question_obj.topic.name)
                )
                for resp in suggested_response_list.suggested_responses:
                    db_suggested_response = create_db_suggested_response(
                        resp, question_obj
                    )
                    saved_suggestion = save_suggested_response(db_suggested_response)
                    logger.info("Saved %s", saved_suggestion)
            except:
                logger.exception("Could not save suggestions for %s", question_obj)
