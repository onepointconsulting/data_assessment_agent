from data_assessment_agent.model.db_model import DbSuggestedResponse
from data_assessment_agent.test.provider.question_provider import create_dummy_question


def create_suggestion_response():
    question = create_dummy_question()
    return DbSuggestedResponse(
        title="Yes", subtitle="Yes", body="Yes, confirmed", question=question
    )
