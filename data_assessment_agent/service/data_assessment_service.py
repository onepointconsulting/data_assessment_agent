from data_assessment_agent.model.assessment_framework import Question
from data_assessment_agent.service.persistence_service import load_questions

questionnaire_questions = load_questions()


def initial_question() -> Question:
    assert len(questionnaire_questions) > 0
    return questionnaire_questions[0]
