import unittest

from data_assessment_agent.service.yes_no_question_service_openai import (
    create_user_message,
)


class TestDBModel(unittest.TestCase):
    def test_create_user_message(self):
        user_message = create_user_message(
            "Do you have a well defined business strategy?"
        )
        assert user_message is not None


if __name__ == "__main__":
    unittest.main()
