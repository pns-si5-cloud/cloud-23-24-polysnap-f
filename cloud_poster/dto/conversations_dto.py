from typing import List
from pydantic import BaseModel

class Participant(BaseModel):
    user_id: str

class Participants(BaseModel):
    participants: List[Participant]

class Message(BaseModel):
    user_id: str
    text: str