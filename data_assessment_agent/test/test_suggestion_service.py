import unittest

from data_assessment_agent.service.suggestion_service import create_user_message
from data_assessment_agent.test.provider.sentiment_provider import create_sentiment_qa


class TestPersistenceService(unittest.TestCase):
    def test_create_user_message(self):
        question, _ = create_sentiment_qa()
        suggestion_user_message = create_user_message(question)
        assert question in suggestion_user_message


if __name__ == "__main__":
    unittest.main()
