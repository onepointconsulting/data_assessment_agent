from typing import Union
from pydantic import BaseModel, Field


class ServerMessage(BaseModel):
    response: str = Field(..., description="The response to be sent to the client")
    sources: Union[str, None] = Field(
        default=None, description="The sources related to the response."
    )
    sessionId: str = Field(..., description="The application's source identifier")
