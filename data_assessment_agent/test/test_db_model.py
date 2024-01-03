import unittest

from data_assessment_agent.model.db_model import Topic, create_questionnaire_status
from data_assessment_agent.test.provider.question_provider import create_dummy_question
from data_assessment_agent.test.provider.suggestion_provider import (
    create_suggestion_response,
)
from data_assessment_agent.test.provider.topic_provider import create_analytics_topic


class TestDBModel(unittest.TestCase):
    def test_topic(self):
        topic = create_analytics_topic()
        json_schema = topic.model_json_schema()
        assert json_schema is not None

    def test_topic_no_desc(self):
        topic = Topic(name="Advanced Analytics")
        json_schema = topic.model_json_schema()
        assert json_schema is not None

    def test_topic_question(self):
        question = create_dummy_question()
        json_schema = question.model_json_schema()
        assert question.topic is not None
        assert json_schema is not None

    def test_create_questionnaire_status(self):
        session_id = "test"
        question = create_dummy_question()
        questionnaire_status = create_questionnaire_status(session_id, question)
        assert questionnaire_status is not None

    def test_create_db_suggested_response(self):
        suggested_response = create_suggestion_response()
        assert suggested_response.question is not None
        copy = suggested_response.model_copy()
        assert copy.title == suggested_response.title
        assert copy.question.question == suggested_response.question.question


if __name__ == "__main__":
    unittest.main()
