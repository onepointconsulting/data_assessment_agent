from typing import List
from pydantic import BaseModel, Field


class ClosestSuggestion(BaseModel):
    suggestion: str = Field(..., description="The closest suggestion to the answer")


closest_suggestion_spec = {
    "name": "closest_suggestion",
    "description": "The closest suggestion to the answer",
    "type": "object",
    "parameters": ClosestSuggestion.model_json_schema(),
}
