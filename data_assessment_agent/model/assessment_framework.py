from typing import List, Dict
from pydantic import BaseModel, Field


class Question(BaseModel):
    category: str = Field(..., description="The question subcategory")
    question: str = Field(..., description="The actual question")
    score: int = Field(..., description="The question score")


class AssessmentFramework(BaseModel):
    categories: Dict[str, List[Question]] = Field(
        ..., description="The questions by section in the whole framework"
    )
