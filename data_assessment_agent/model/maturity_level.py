from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field


class MaturityLevelEnum(str, Enum):
    NO_CAPABILITY = "No capability"
    AD_HOC = "Ad-hoc"
    REPEATABLE = "Repeatable"
    DEFINED = "Defined"
    MANAGED = "Managed"
    OPTIMIZED = "Optimized"


MATURITY_LEVEL_DICT = {
    MaturityLevelEnum.NO_CAPABILITY: 1,
    MaturityLevelEnum.AD_HOC: 2,
    MaturityLevelEnum.REPEATABLE: 3,
    MaturityLevelEnum.DEFINED: 4,
    MaturityLevelEnum.MANAGED: 5,
    MaturityLevelEnum.OPTIMIZED: 6,
}

MATURITY_LEVEL_DICT_INVERTED = {v: k for k, v in MATURITY_LEVEL_DICT.items()}


class CategoryMaturityLevel(BaseModel):
    category: str = Field(
        ...,
        description="The category for which a maturity level is to be determined. Examples are: Data Security, Data Privacy, Data Assets, Dataops, Data Acquisition, Business Alignment",
    )
    maturity_level: MaturityLevelEnum = Field(
        ..., description="The maturity level to be used to assess the category"
    )
    reasoning: str = Field(..., description="The reasoning behind the classification.")
    missing_information_comments: Optional[str] = Field(
        ...,
        description="Details whether some extra information for the assessment would be helpful.",
    )


class MaturityLevelResponse(BaseModel):
    maturity_levels: List[CategoryMaturityLevel] = Field(
        ...,
        description="The list of categories with the corresponding maturity levels and reasoning around it.",
    )


class ScoredMaturityLevelResponse(MaturityLevelResponse):
    score: float = Field(..., description="The overall score as average of all scores")
    maturity_level: MaturityLevelEnum = Field(
        ..., description="The overall maturity level"
    )


maturity_level_spec = {
    "name": "maturity_level",
    "description": "Assigns maturity levels to different categories based on the answers to a set of questions",
    "type": "object",
    "parameters": MaturityLevelResponse.model_json_schema(),
}
