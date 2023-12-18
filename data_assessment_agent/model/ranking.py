from typing import List
from pydantic import BaseModel, Field


class RankedQuestionsResponse(BaseModel):
    ranked_questions: List[str] = Field(
        ...,
        description="The list of ranked questions according to a specific topic",
    )


question_ranking_spec = {
    "name": "question_ranking",
    "description": "Ranks questions",
    "type": "object",
    "parameters": RankedQuestionsResponse.model_computed_fields(),
}
