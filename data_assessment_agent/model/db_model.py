from typing import Union, Optional
from pydantic import BaseModel, Field

from data_assessment_agent.model.sentiment import Sentiment
from data_assessment_agent.model.assessment_framework import Question as DomainQuestion
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
