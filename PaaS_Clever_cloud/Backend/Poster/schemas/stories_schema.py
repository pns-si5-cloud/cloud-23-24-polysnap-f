from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl

class Viewer(BaseModel):
    user_id: str = Field(..., example="string")

class StoryCreate(BaseModel):
    user_id: str = Field(..., example="string")
    image_url: str = Field(..., example="http://example.com/image.jpg")
    viewers: List[Viewer] = Field(
        ...,
        example=[
            {"user_id": "string"},
            {"user_id": "string"}],
    )
    duration: Optional[int] = Field(24, example=24)  # Durée en heures

class Story(BaseModel):
    user_id: str
    image_url: HttpUrl

class StoriesResponse(BaseModel):
    stories: List[Story]
