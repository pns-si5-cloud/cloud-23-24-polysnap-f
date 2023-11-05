from typing import Optional, List
from fastapi import APIRouter, Request, HTTPException, Depends, Form
from config import BUCKET_NAME, GOOGLE_TOPIC_ID
from schemas import Participant, ConversationCreate, Message, UserResponse, StoryCreate, UserIdResponse
from services import send_post_request, add_message_to_conversation_db, mark_message_as_read, create_conversation_db, generate_upload_signed_url_v4
from services import publish_message_to_topic, get_user_db, create_story_db, get_users_db

router = APIRouter()

@router.post("/conversations/{conversation_id}/messages")
async def add_message_to_conversation(conversation_id: str, message: Message):
    try:
        result = await add_message_to_conversation_db(conversation_id, message)
        try:
            # Tentez de publier le message
            publish_message_to_topic(result, GOOGLE_TOPIC_ID)
        except Exception as e:
            # Si la publication échoue, envoyez la requête
            print(f"Failed to publish message: {str(e)}")
            await send_post_request(result)
        
        return {"message": "Data stored successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store message: {str(e)}")
    
@router.put("/conversations/{conversation_id}/messages/{message_id}/read")
async def mark_message_as_read_in_conversation(conversation_id: str, message_id: str, user: Participant):
    try:
        await mark_message_as_read(conversation_id, message_id, user.user_id)
        return {"message": "Message marked as read"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to mark message as read: {str(e)}")

@router.post("/conversations")
async def create_conversation(conversation: ConversationCreate):
    if not conversation.participants or len(conversation.participants) < 2:
        raise HTTPException(status_code=400, detail="Invalid participants list")
    try:
        #conversation_id = await create_conversation_db(conversation.name, [p.user_id for p in conversation.participants], conversation.read_duration)
        conversation_id = await create_conversation_db(conversation)
        return {"message": "Conversation created successfully", "conversation_id": str(conversation_id)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create conversation: {str(e)}")

@router.get("/upload-url")
async def get_upload_url(content_type: str):
    try:
        blob_name, signed_url = generate_upload_signed_url_v4(BUCKET_NAME,content_type)
        return {"signed_url": signed_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate signed URL: {str(e)}")

@router.get("/users", response_model=List[UserIdResponse])
async def get_users():
    try:
        users = await get_users_db()
        return [UserIdResponse(**user) for user in users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get users: {str(e)}")
    
@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    try:
        user = await get_user_db(user_id)
        return UserResponse.from_mongo(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user: {str(e)}")

@router.post("/stories")
async def create_story(story: StoryCreate):
    try:
        story_id = await create_story_db(story)
        return {"message": "Story created successfully", "story_id": str(story_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create story: {str(e)}")