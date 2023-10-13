from datetime import datetime
from bson import ObjectId
import motor.motor_asyncio
from config import MONGODB_URI, DATABASE_NAME, COLLECTION_USER, COLLECTION_CONVERSATION

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
db = client[DATABASE_NAME]
conversations_collection = db[COLLECTION_CONVERSATION]
user_collection = db[COLLECTION_USER]

async def create_conversation_db(participants):
    print(MONGODB_URI)
    print(DATABASE_NAME)
    print(COLLECTION_USER)
    print(COLLECTION_CONVERSATION)
    new_conversation = {
        "participants": participants,
        "messages": []
    }
    
    result = await conversations_collection.insert_one(new_conversation)
    return result.inserted_id

async def add_message_to_conversation_db(conversation_id, sender_id, text):
    conversation_obj_id = ObjectId(conversation_id)
    message = {
        "sender": sender_id,
        "timestamp": datetime.utcnow().isoformat(),
        "text": text,
        "image": None
    }

    await conversations_collection.update_one(
        {"_id": conversation_obj_id},
        {"$push": {"messages": message}}
    )

async def store_data_base(json_data):
    collection = db["messages"]
    result = await collection.insert_one(json_data)
    return result.inserted_id
