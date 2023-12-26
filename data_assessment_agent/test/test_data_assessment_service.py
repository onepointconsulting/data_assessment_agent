import unittest

from data_assessment_agent.config.toml_support import prompts
from data_assessment_agent.service.ranking_service import create_user_message
from data_assessment_agent.test.provider.ranking_prompt_provider import (
    ranking_prompt_provider,
)


class TestConfig(unittest.TestCase):
    def test_create_user_message(self):
        topic, question_answers, ranking_questions = ranking_prompt_provider()
        res = create_user_message(topic, question_answers, ranking_questions)
        assert res is not None
        assert ranking_questions in res
        assert question_answers in res
        assert topic in res


if __name__ == "__main__":
    unittest.main()
