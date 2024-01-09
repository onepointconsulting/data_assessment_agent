import unittest

from data_assessment_agent.service.ranking_service import create_user_message
from data_assessment_agent.test.provider.ranking_prompt_provider import (
    ranking_prompt_provider,
)
from data_assessment_agent.service.data_assessment_service import (
    selected_random_question,
)


class TestConfig(unittest.TestCase):
    def test_create_user_message(self):
        topic, question_answers, ranking_questions = ranking_prompt_provider()
        res = create_user_message(topic, question_answers, ranking_questions)
        assert res is not None
        assert ranking_questions in res
        assert question_answers in res
        assert topic in res

    def test_select_random_question(self):
        questions = ["What is the meaning of life?", "Why are we on earth?"]
        topic = "existential"
        question = selected_random_question(questions, topic)
        assert question is not None
        assert question.question in questions
        assert question.category == topic


if __name__ == "__main__":
    unittest.main()
