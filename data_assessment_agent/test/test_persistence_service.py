import unittest

from data_assessment_agent.service.ranking_service import create_topics_user_message
from data_assessment_agent.test.provider.question_provider import (
    create_question_answers,
)
from data_assessment_agent.test.provider.topic_provider import create_topic_list


class TestPersistenceService(unittest.TestCase):
    def test_create_topics_user_message(self):
        topics = "\n".join(create_topic_list())
        question_answers = create_question_answers()
        user_message = create_topics_user_message(question_answers, topics)
        assert user_message is not None
        assert "START RANKING_TOPICS" in user_message
        assert "Advanced Analytics" in user_message


if __name__ == "__main__":
    unittest.main()
