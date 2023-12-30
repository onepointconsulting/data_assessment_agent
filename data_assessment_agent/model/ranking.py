from typing import List
from pydantic import BaseModel, Field


class RankedQuestionsResponse(BaseModel):
    ranked_questions: List[str] = Field(
        ...,
        description="The list of ranked questions according to a specific topic. Should have not more than 4 items",
    )


class RankedTopicsResponse(BaseModel):
    ranked_topics: List[str] = Field(
        ...,
        description="The list of ranked topics according to a set of responses. Should have not more than 4 items",
    )


question_ranking_spec = {
    "name": "question_ranking",
    "description": "Ranks questions",
    "type": "object",
    "parameters": RankedQuestionsResponse.model_json_schema(),
}

topic_ranking_spec = {
    "name": "topic_ranking",
    "description": "Ranks topics according to a set of questions",
    "type": "object",
    "parameters": RankedTopicsResponse.model_json_schema(),
}

if __name__ == "__main__":
    print(RankedQuestionsResponse.model_json_schema())
    print(RankedTopicsResponse.model_json_schema())
