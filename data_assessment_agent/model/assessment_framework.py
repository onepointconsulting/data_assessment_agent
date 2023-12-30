from typing import List, Dict, Optional
from pydantic import BaseModel, Field


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


class AssessmentFramework(BaseModel):
    categories: Dict[str, List[Question]] = Field(
        ..., description="The questions by section in the whole framework"
    )
    preferred_order: Dict[str, int] = Field(
        ..., description="The preferred order for each of the categories"
    )
