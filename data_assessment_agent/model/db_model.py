from typing import Union, Optional, List
from datetime import datetime

from pydantic import BaseModel, Field

from data_assessment_agent.model.sentiment import Sentiment
from data_assessment_agent.model.assessment_framework import (
    Question as DomainQuestion,
    SuggestedResponse,
)
from data_assessment_agent.config.log_factory import logger


class Topic(BaseModel):
    id: Union[int, None] = Field(default=None, description="The topic id")
    name: str = Field(..., description="The topic name")
    description: Union[str, None] = Field(
        default=None, description="The topic description"
    )
    question_amount: Union[int, None] = Field(
        default=5, description="The amount of questions in this topic"
    )
    preferred_topic_order: Union[int, None] = Field(
        default=0, description="The field used to order the topics"
    )


class Question(BaseModel):
    id: Union[int, None] = Field(default=None, description="The question id")
    question: str = Field(..., description="The question to ask the user")
    score: int = Field(..., description="What kind of score is asked from the user")
    topic: Topic = Field(..., description="The topic ttp which the question belongs")
    preferred_order: Union[int, None] = Field(default=0, description="The question id")
    yes_no_question: bool = Field(
        default=False,
        description="Whether the question can be answered with a you, no or maybe answer",
    )
    scored: bool = Field(
        default=True, description="Tells us whether a question is scored or not"
    )


class DbSuggestedResponse(SuggestedResponse):
    id: Union[int, None] = Field(default=None, description="The suggested response id")
    question: Question = Field(
        ..., description="The question to which this suggested response is associated"
    )


class QuestionnaireStatus(BaseModel):
    id: Union[int, None] = Field(default=None, description="The status id")
    session_id: str = Field(..., description="The session identifier")
    topic: str = Field(..., description="The topic of the question")
    question: str = Field(..., description="The question the user replied")
    answer: Optional[str] = Field(
        default=None, description="The answer given by the user"
    )
    score: Optional[int] = Field(
        default=None, description="The score given to the user's reply"
    )
    sentiment: Optional[str] = Field(
        default=Sentiment.UNKNOWN, description="The score given to the user's reply"
    )
    topic_count: Optional[int] = Field(
        default=None, description="The last topic's current count"
    )
    topic_missing: Optional[int] = Field(
        default=None, description="How many questions missing to finish the topic"
    )
    previous_answer_count: Optional[int] = Field(
        default=None, description="How many answers equal to this one were answered"
    )


class QuestionnaireCounts(BaseModel):
    topic: str = Field(..., description="The current topic for the current session")
    question_count: int = Field(
        ..., description="The count of finished questions in the last topic"
    )
    question_total: int = Field(
        ..., description="The total questions in the current topic"
    )
    finished_topic_count: int = Field(
        ..., description="The total number of finished topics"
    )
    topic_total: int = Field(..., description="The total count of topics")


class TopicScore(BaseModel):
    topic_name: str = Field(..., description="The name of the topic")
    max_score: int = Field(..., description="The maximum score in this topic")
    score: int = Field(..., description="The score for the specific topic")


class TopicScoreResult(BaseModel):
    session_id: str = Field(..., description="The session identifier")
    topic_scores: List[TopicScore] = Field(..., description="The list of topic scores")


class QuestionScore(BaseModel):
    score: int = Field(..., description="The score attained by the question")
    max_score: int = Field(..., description="The maximum possible score")
    sentiment_name: str = Field(..., description="The name of the sentiment")
    topic_name: str = Field(..., description="The name of the topic")
    session_id: str = Field(..., description="The current session id")


class SessionScores(BaseModel):
    session_id: str = Field(..., description="The session id")
    topic_scores: List[TopicScore] = Field(..., description="The topic scores")


class TotalScore(BaseModel):
    total_score: int = Field(..., description="The sum of all question scores")
    max_score: int = Field(..., description="The maximum possible score")
    pct_score: float = Field(
        ..., description="The percentage of the score relatively to the final score"
    )


class QuizzMode(BaseModel):
    id: Union[int, None] = Field(default=None, description="The mode identifier")
    name: str = Field(..., description="The name of the quizz mode")
    question_count: int = Field(..., description="The number of questions in this mode")


class SelectedConfiguration(BaseModel):
    session_id: str = Field(..., description="The session identifier")
    topic_list: List[str] = Field(
        ..., description="The list of topics which the user selected"
    )
    quiz_mode_name: str = Field(..., description="The name of the quiz mode")


def create_questionnaire_status(
    session_id: str, question: Union[Question, DomainQuestion, QuestionnaireStatus]
):
    logger.info("create_questionnaire_status question type: %s", type(question))
    if isinstance(question, Question):
        topic_name = question.topic.name
    elif isinstance(question, DomainQuestion):
        topic_name = question.category
    elif isinstance(question, QuestionnaireStatus):
        topic_name = question.topic
    return QuestionnaireStatus(
        session_id=session_id, topic=topic_name, question=question.question
    )


def create_db_suggested_response(
    suggested_response: SuggestedResponse, question: Question
) -> DbSuggestedResponse:
    return DbSuggestedResponse(
        title=suggested_response.title,
        subtitle=suggested_response.subtitle,
        body=suggested_response.body,
        question=question,
    )


class SessionReport(BaseModel):
    topic: str = Field(..., description="The question's topic")
    question: str = Field(..., description="The question")
    answer: str = Field(..., description="The answer to the question")
    score: int = Field(..., description="The calculated score")
    sentiment: str = Field(
        ..., description="The sentiment of the answer towards the question"
    )
    created_at: datetime = Field(..., description="The creation timestamp")
    updated_at: datetime = Field(..., description="The update timestamp")


class QAScored(BaseModel):
    topic: str = Field(..., description="The topic of the QA")
    question: str = Field(..., description="The single question")
    answer: str = Field(..., description="The single answer")
    score: int = Field(
        ..., description="The score to this answer related to this question"
    )
