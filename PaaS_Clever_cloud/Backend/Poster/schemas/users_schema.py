from pydantic import BaseModel

class User(BaseModel):
    user_id: str
    conversations: list = []

class UserIdResponse(BaseModel):
    user_id: str
    
class UserResponse(BaseModel):
    user_id: str
    conversations: list

    @classmethod
    def from_mongo(cls, user):
        return cls(
            user_id=user['user_id'],
            conversations=[str(_id) for _id in user['conversations']],
        )
