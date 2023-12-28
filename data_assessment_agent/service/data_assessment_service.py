from data_assessment_agent.model.assessment_framework import Question
from data_assessment_agent.service.persistence_service import (
    load_questions,
    select_last_question,
    select_remaining_questions,
    select_answered_questions_in_topic
)
from data_assessment_agent.service.ranking_service import rank_questions

questionnaire_questions = load_questions()


def initial_question() -> Question:
    assert len(questionnaire_questions) > 0
    return questionnaire_questions[0]


def select_next_question(session_id: str) -> Question:
    first_question = select_last_question(session_id)
    if first_question is None:
        return initial_question()
    elif first_question.answer is None:
        # This means that the question has not been answered yet
        return first_question
    elif first_question.answer is not None:
        # Case: unanswered question
        # Get the topic and the count
        topic = first_question.topic
        missing_in_topic = first_question.topic_missing
        if missing_in_topic > 0:
            # Get all previously answered questions
            question_answers_list = select_answered_questions_in_topic(session_id, topic)
            question_answers = "\n".join(question_answers_list)
            # There are missing questions in this topic
            questions = select_remaining_questions(session_id, topic)
            ranking_questions = "\n".join(questions)
            # Let ChatGPT sort the questions
            ranked_questions = rank_questions(topic, question_answers, ranking_questions)
            if len(ranked_questions) > 0:
                return Question(category=topic, question=ranked_questions[0], score=0)
            return None
        else:
            # There are no questions left. Select the next topic
            pass
