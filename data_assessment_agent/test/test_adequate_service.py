import unittest

from data_assessment_agent.service.suggestion_proximity_service import (
    create_user_message,
)
from data_assessment_agent.test.provider.suggestion_provider import (
    create_multiple_suggestions,
)


class TestDBModel(unittest.TestCase):
    def test_question(self):
        answer, suggestions = create_multiple_suggestions()
        response = create_user_message(answer, suggestions)
        assert "The data transformations in our system are really complex" in response


if __name__ == "__main__":
    unittest.main()
