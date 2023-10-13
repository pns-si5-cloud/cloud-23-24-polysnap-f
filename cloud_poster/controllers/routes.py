from fastapi import APIRouter, Request, HTTPException, Depends, Form
from fastapi.templating import Jinja2Templates

from dto import Participants, Message
from services import store_data_base, send_post_request, add_message_to_conversation_db, create_conversation_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/form")
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@router.post("/form")
async def post_form(message: str = Form(...), idSender: str = Form(...), idReceiver: str = Form(...)):
    try:
        await send_post_request(message, idSender, idReceiver)
        json_data = {"idSender": idSender, "idReceiver": idReceiver, "message": message}
        id_collection = await store_data_base(json_data)
        return {"message": "Data stored successfully", "id": str(id_collection)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store message: {str(e)}")

@router.post("/conversations/{conversation_id}/messages")
async def add_message_to_conversation(conversation_id: str, message: Message):
    try:
        await add_message_to_conversation_db(conversation_id, message.user_id, message.text)
        return {"message": "Data stored successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store message: {str(e)}")

@router.post("/conversations")
async def create_conversation(participants: Participants):
    if not participants or len(participants.participants) < 2:
        raise HTTPException(status_code=400, detail="Invalid participants list")
    try:
        conversation_id = await create_conversation_db([p.user_id for p in participants.participants])
        return {"message": "Conversation created successfully", "conversation_id": str(conversation_id)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create conversation: {str(e)}")
