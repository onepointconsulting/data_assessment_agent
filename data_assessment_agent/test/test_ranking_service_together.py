import unittest

from data_assessment_agent.service.ranking_service_together import create_user_message
from data_assessment_agent.test.provider.question_provider import (
    create_question_answers,
    create_ranking_questions,
)
from data_assessment_agent.test.provider.topic_provider import create_topic_title


class TestDateUtils(unittest.TestCase):
    def test_create_user_message(self):
        question_answers = create_question_answers()
        topic = create_topic_title()
        ranking_questions = create_ranking_questions()
        user_message = create_user_message(topic, question_answers, ranking_questions)
        assert user_message is not None
