from data_assessment_agent.model.db_model import QuestionnaireStatus


def create_questionnaire_status() -> QuestionnaireStatus:
    return QuestionnaireStatus(
        session_id="dummy",
        topic="Business Alignment",
        question="What are the organization's short-term and long-term business goals?",
        answer="",
        score=0,
    )
