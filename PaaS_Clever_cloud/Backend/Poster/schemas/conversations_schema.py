from typing import List, Optional
from pydantic import BaseModel, Field

class Participant(BaseModel):
    user_id: str = Field(..., example="string")

class ConversationCreate(BaseModel):
    name: str = Field(..., example="string")
    participants: List[Participant] = Field(
        ...,
        example=[
            {"user_id": "string"},
            {"user_id": "string"},
        ]
    )
    read_duration: Optional[int] = 60

class Message(BaseModel):
    user_id: str
    text: str
    url: Optional[str] = ''
    smoke: Optional[bool] = True