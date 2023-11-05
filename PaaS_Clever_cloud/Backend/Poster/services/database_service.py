from datetime import datetime
from bson import ObjectId
import motor.motor_asyncio
from config import MONGODB_URI, DATABASE_NAME, COLLECTION_USER, COLLECTION_CONVERSATION, COLLECTION_STORY
from schemas import ConversationCreate, StoryCreate, User

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
db = client[DATABASE_NAME]
conversations_collection = db[COLLECTION_CONVERSATION]
user_collection = db[COLLECTION_USER]
stories_collection = db[COLLECTION_STORY]

async def create_conversation_db(conversation : ConversationCreate):
    participants = [p.user_id for p in conversation.participants]
    name = conversation.name
    read_duration = conversation.read_duration
    if read_duration is None:
        read_duration = 60

    if len(participants) < 2:
        raise ValueError("Invalid participants list")

    for participant in participants:
        if participants.count(participant) > 1:
            raise ValueError("Invalid participants list")
    
    for participant in participants:
        #check if user exists in user collection, if not, add it and create an empty conversations array
        if not await user_collection.find_one({"user_id": participant}):
            await user_collection.insert_one({"user_id": participant, "conversations": []})

    new_conversation = {
        "name" : name,
        "participants": participants,
        "messages": [],
        "read_duration": read_duration # in minutes
    }

    result = await conversations_collection.insert_one(new_conversation)

    for participant in participants:
        await user_collection.update_one(
            {"user_id": participant},
            {"$push": {"conversations": result.inserted_id}}
        )

    return result.inserted_id

async def add_message_to_conversation_db(conversation_id, message):
    conversation_obj_id = ObjectId(conversation_id)
    message = {
        "_id": ObjectId(),
        "conversation_id": conversation_obj_id,
        "sender": message.user_id,
        "timestamp": datetime.utcnow().isoformat(),
        "text": message.text,
        "image": message.url,
        "read_by": [message.user_id],
        "smoke": message.smoke
    }

    await conversations_collection.update_one(
        {"_id": conversation_obj_id},
        {"$push": {"messages": message}}
    )

    return message

async def mark_message_as_read(conversation_id, message_id, user_id):
    conversation_obj_id = ObjectId(conversation_id)
    await conversations_collection.update_one(
        {"_id": conversation_obj_id, "messages._id": ObjectId(message_id)},
        {"$addToSet": {"messages.$.read_by": user_id}}
    )

async def get_users_db():
    users = []
    async for user in user_collection.find({}, {"_id": 0, "user_id": 1}):
        users.append(user)
    return users

async def get_user_db(user_id):
    user = await user_collection.find_one({"user_id": user_id}, {"_id": 0, "user_id": 1, "conversations": 1})
    if not user:
        user = User(user_id=user_id).dict()
        await user_collection.insert_one(user)
        return user

    return user

async def create_story_db(story: StoryCreate):
    user_id = story.user_id
    image_url = story.image_url
    viewers = [viewer.user_id for viewer in story.viewers]
    duration = story.duration


    if duration is None:
        duration = 24

    # Create story object
    new_story = {
        "user_id": user_id,
        "image_url": image_url,
        "timestamp": datetime.utcnow().isoformat(),
        "viewers": viewers,
        "duration": duration
    }

    # Insert story in story collection
    result = await stories_collection.insert_one(new_story)

    # Add story to my_stories of user
    await user_collection.update_one(
        {"user_id": user_id},
        {"$push": {"my_stories": result.inserted_id}}
    )

    # Add story to viewable_stories of viewers
    for viewer in viewers:
        await user_collection.update_one(
            {"user_id": viewer},
            {"$push": {"viewable_stories": result.inserted_id}}
        )

    return result.inserted_id