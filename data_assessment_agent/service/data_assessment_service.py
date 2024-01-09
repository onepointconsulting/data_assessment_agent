import random
from typing import Union, List
from data_assessment_agent.model.assessment_framework import Question
from data_assessment_agent.service.persistence_service import (
    load_questions,
    select_remaining_questions,
    select_answered_questions_in_topic,
    select_answered_questions_in_session,
    select_remaining_topics,
)
from data_assessment_agent.service.persistence_service_async import (
    select_last_question,
    select_initial_question_from_topic,
)
from data_assessment_agent.service.ranking_service import rank_questions, rank_topics
from data_assessment_agent.config.log_factory import logger

questionnaire_questions = load_questions()


def initial_question() -> Question:
    assert len(questionnaire_questions) > 0
    db_question = questionnaire_questions[0]
    return Question(
        question=db_question.question,
        category=db_question.topic.name,
        score=db_question.score if db_question.score is not None else 0,
        initial=True,
    )


async def select_next_question(session_id: str) -> Union[Question, None]:
    first_question = await select_last_question(session_id)
    if first_question is None:
        return initial_question()
    elif first_question.answer is None and first_question.previous_answer_count == 0:
        # This means that the question has not been answered yet
        return create_question(first_question.topic, first_question.question)
    else:
        # Case: unanswered question or the question was already answered and we need a new one
        # Get the topic and the count
        topic = first_question.topic
        missing_in_topic = first_question.topic_missing
        if missing_in_topic > 0:
            logger.info("There are missing questions in topic")
            # Get all previously answered questions
            question_answers_list = select_answered_questions_in_topic(
                session_id, topic
            )
            question_answers = "\n".join(question_answers_list)
            logger.info("Answered questions: %s", question_answers)
            # There are missing questions in this topic
            questions = select_remaining_questions(session_id, topic)
            if questions is None:
                return None
            logger.info("== Remaining questions ==")
            for q in questions:
                logger.info(q)
            ranking_questions = "\n".join(questions)
            # Let ChatGPT sort the questions
            ranked_questions = await rank_questions(
                topic, question_answers, ranking_questions
            )
            while len(ranked_questions) > 0:
                candidate_question = ranked_questions[0]
                if candidate_question in questions:
                    return create_question(topic, candidate_question)
                ranked_questions = ranked_questions[1:]
            return None
        else:
            logger.info("Selecting next topic")
            # There are no questions left. Select the next topic
            # Get all question and answers from this session
            # Get all topics covered in this session
            question_answers_list = select_answered_questions_in_session(session_id)
            question_answers = "\n".join(question_answers_list)
            ranking_topics = select_remaining_topics(session_id)
            if len(ranking_topics) == 0:
                # We reached probably the end of the questionnaire
                return Question(question="", category="", score=0, final=True)
            ranking_topics_str = "\n".join(ranking_topics)
            # Ask ChatGPT to rank the topics
            logger.info("ranking_topics_str: %s", ranking_topics_str)
            missing_topics = await rank_topics(question_answers, ranking_topics_str)
            if len(missing_topics) == 0:
                return None
            selected_topic = missing_topics[0]
            logger.info("selected topic: %s", selected_topic)
            # Start with a random question in this topic
            selected_question = await select_initial_question_from_topic(
                selected_topic, session_id
            )
            return create_question(
                selected_question.topic.name, selected_question.question
            )


async def safe_question_rank(
    topic: str, question_answers: str, ranking_questions: str, questions: List[str]
) -> Question:
    ranked_questions = await rank_questions(topic, question_answers, ranking_questions)
    while len(ranked_questions) > 0:
        candidate_question = ranked_questions[0]
        if candidate_question in questions:
            return create_question(topic, candidate_question)
        ranked_questions = ranked_questions[1:]
    if len(questions) > 0:
        # ChatGPT must have failed to rank the questions
        # Select random question
        return selected_random_question(questions, topic)
    return None


def selected_random_question(questions: List[str], topic: str) -> Question:
    selected_question = random.choice(questions)
    return Question(category=topic, question=selected_question, score=0)


def create_question(topic_name: str, question: str) -> Question:
    return Question(
        category=topic_name,
        question=question,
        score=0,
        question_count=-1,
        total_questions_in_topic=-1,
    )
