import unittest

from data_assessment_agent.service.clarification_service import create_user_message
from data_assessment_agent.test.provider.clarification_provider import (
    clarification_data_1,
)


class TestPersistenceService(unittest.TestCase):
    def test_create_user_message(self):
        question, topic = clarification_data_1()
        sentiment_user_message = create_user_message(question, topic)
        assert sentiment_user_message is not None
        print(sentiment_user_message)


if __name__ == "__main__":
    unittest.main()
