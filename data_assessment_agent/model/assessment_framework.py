from typing import List, Dict, Optional, Union
from pydantic import BaseModel, Field


class SuggestedResponse(BaseModel):
    title: str = Field(..., description="The title of the suggested message")
    subtitle: Union[str, None] = Field(
        ..., description="The secondary title of the suggested message"
    )
    body: str = Field(
        ...,
        description="The whole text of the suggested response. Should be no more that 1024 characters long",
    )


class Question(BaseModel):
    category: str = Field(..., description="The question subcategory")
    question: str = Field(..., description="The actual question")
    score: int = Field(..., description="The question score")
    question_count: Optional[int] = Field(
        default=None, description="Answered question count out of n in topic"
    )
    total_questions_in_topic: Optional[int] = Field(
        default=None, description="Question number out of n in topic"
    )
    finished_topic_count: Optional[int] = Field(
        default=None, description="The count of the finished topics"
    )
    topic_total: Optional[int] = Field(
        default=None, description="The total amount of topics"
    )
    initial: bool = Field(
        default=False, description="Whether this is the first question ever or not."
    )
    final: bool = Field(
        default=False,
        description="Whether we have reached the end of the questionnaire",
    )
    suggestions: List[SuggestedResponse] = Field(
        default=[], description="The suggested responses for this question"
    )


class AssessmentFramework(BaseModel):
    categories: Dict[str, List[Question]] = Field(
        ..., description="The questions by section in the whole framework"
    )
    preferred_order: Dict[str, int] = Field(
        ..., description="The preferred order for each of the categories"
    )


class SessionMessage(BaseModel):
    next_question: Question = Field(
        ..., description="The next question to be sent to the client"
    )
    sid: str = Field(..., description="The websocket room session id")
    session_id: str = Field(..., description="The application's session identifier")


class SuggestedResponseList(BaseModel):
    suggested_responses: List[SuggestedResponse] = Field(
        ..., description="The list with suggested responses"
    )


suggested_response_list_spec = {
    "name": "suggested_response",
    "description": "Suggested responses for a specific question",
    "type": "object",
    "parameters": SuggestedResponseList.model_json_schema(),
}
