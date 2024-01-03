from typing import Union, List
from pydantic import BaseModel, Field

from data_assessment_agent.model.assessment_framework import SuggestedResponse


class ServerMessage(BaseModel):
    response: str = Field(..., description="The response to be sent to the client")
    sources: Union[str, None] = Field(
        default=None, description="The sources related to the response."
    )
    sessionId: str = Field(..., description="The application's source identifier")
    suggestions: List[SuggestedResponse] = Field(
        default=[], description="The list of suggested responses"
    )
