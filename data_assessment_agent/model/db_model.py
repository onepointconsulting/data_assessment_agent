from typing import Union, Optional
from pydantic import BaseModel, Field

from data_assessment_agent.config.log_factory import logger


class Topic(BaseModel):
    id: Union[int, None] = Field(default=None, description="The topic id")
    name: str = Field(..., description="The topic name")
    description: Union[str, None] = Field(
        default=None, description="The topic description"
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
    score: Optional[str] = Field(
        default=None, description="The score given to the user's reply"
    )
    topic_count: Optional[int] = Field(
        default=None, description="The last topic's current count"
    )
    topic_missing: Optional[int] = Field(
        default=None, description="How many questions missing to finish the topic"
    )


def create_questionnaire_status(
    session_id: str, question: Union[Question, QuestionnaireStatus]
):
    logger.info("create_questionnaire_status question type: %s", type(question))
    topic_name = (
        question.topic.name if isinstance(question, Question) else question.topic
    )
    return QuestionnaireStatus(
        session_id=session_id, topic=topic_name, question=question.question
    )
