import unittest

from data_assessment_agent.service.suggestion_proximity_service import (
    create_user_message,
)
from data_assessment_agent.test.provider.question_provider import (
    create_question_answer_topic,
)


class TestDBModel(unittest.TestCase):
    def test_question(self):
        topic, question, answer = create_question_answer_topic()
        response = create_user_message(question, answer, topic)
        assert (
            "Determine whether the answer to the question in topic `Business Alignment` mentioned below is adequate or not"
            in response
        )


if __name__ == "__main__":
    unittest.main()
