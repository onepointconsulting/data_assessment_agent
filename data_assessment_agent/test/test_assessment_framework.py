import unittest

from data_assessment_agent.model.assessment_framework import Question


class TestDBModel(unittest.TestCase):
    def test_question(self):
        Question(
            question="Are data domain, data ownership and stewardship roles defined and communicated in the charter?",
            category="Data Governance",
            score=0,
        )


if __name__ == "__main__":
    unittest.main()
