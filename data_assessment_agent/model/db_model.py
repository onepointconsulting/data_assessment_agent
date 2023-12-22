from typing import Union
from pydantic import BaseModel, Field


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
    answer: str = Field(..., description="The answer given by the user")
    score: str = Field(..., description="The score given to the user's reply")
