from typing import Union
from pydantic import BaseModel


class ServerMessage(BaseModel):
    response: str
    sources: Union[str, None]
    sessionId: str
