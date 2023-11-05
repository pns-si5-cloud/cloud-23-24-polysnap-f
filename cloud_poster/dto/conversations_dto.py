from typing import List
from pydantic import BaseModel, Field

class Participant(BaseModel):
    user_id: str

class Participants(BaseModel):
    participants: List[Participant] = Field(
        ...,
        example=[
            {"user_id": "string"},
            {"user_id": "string"},
            {"user_id": "string"}
        ]
    )

class Message(BaseModel):
    user_id: str
    text: str