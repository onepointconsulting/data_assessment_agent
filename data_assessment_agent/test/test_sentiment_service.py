import unittest

from data_assessment_agent.service.sentiment_service import create_user_message
from data_assessment_agent.test.provider.sentiment_provider import create_sentiment_qa


class TestPersistenceService(unittest.TestCase):
    def test_create_user_message(self):
        question, answer = create_sentiment_qa()
        sentiment_user_message = create_user_message(question, answer)
        assert question in sentiment_user_message, sentiment_user_message
        assert answer in sentiment_user_message


if __name__ == "__main__":
    unittest.main()
