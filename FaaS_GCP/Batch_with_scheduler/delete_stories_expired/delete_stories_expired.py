from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
import asyncio
import os
from dotenv import load_dotenv
import functions_framework

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_STORY = os.getenv("COLLECTION_STORY")
COLLECTION_USER = os.getenv("COLLECTION_USER")

async def cleanup_batch(story_collection, user_collection,batch_size, skip):
    # Initialize the list that will contain the IDs of the stories updated
    stories_to_remove = []

    # Retrieve and process stories by batch
    async for story in story_collection.find().skip(skip).limit(batch_size):
        current_utc_time = datetime.utcnow()

        story_time = datetime.fromisoformat(story['timestamp'])
        expiration_time = story_time + timedelta(minutes=story['duration'])

        if current_utc_time > expiration_time:
            stories_to_remove.append(story['_id'])
        stories_to_remove.append(story['_id'])

    if stories_to_remove:
         # Delete stories from story collection
        await story_collection.delete_many({"_id": {"$in": stories_to_remove}})

        # Update user collection - remove these stories from my_stories and viewable_stories
        await user_collection.update_many(
            {},
            {
                "$pull": {
                    "my_stories": {"$in": stories_to_remove},
                    "viewable_stories": {"$in": stories_to_remove}
                }
            }
        )

    # return stories deleted
    return stories_to_remove

def run_async_function(func):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(func(*args, **kwargs))
        finally:
            loop.close()
    return wrapper


@functions_framework.http
@run_async_function
async def schedule_cleanup(request):

    # For more information about CORS and CORS preflight requests, see:
    # https://developer.mozilla.org/en-US/docs/Glossary/Preflight_request

    # Set CORS headers for the preflight request
    if request.method == "OPTIONS":
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }

        return ("", 204, headers)
    
    # Set CORS headers for the main request
    headers = {"Access-Control-Allow-Origin": "*"}

    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    story_collection = db[COLLECTION_STORY]
    user_collection = db[COLLECTION_USER]

    batch_size = 10000  # Nombre de storys par lot
    # Calculate the number of batches required to process all stories
    total_stories = await story_collection.count_documents({})
    num_batches = (total_stories + batch_size - 1) // batch_size

    total_stories_deleted = []

    # Create a list of tasks to run in parallel
    tasks = [
        cleanup_batch(story_collection, user_collection, batch_size, i * batch_size)
        for i in range(num_batches)
    ]

    # Execute the tasks in parallel
    results = await asyncio.gather(*tasks)

    # Aggregate the IDs of the stories updated
    for batch_result in results:
        total_stories_deleted.extend(batch_result)

    # Convert ObjectId to string
    total_stories_deleted = [str(oid) for oid in total_stories_deleted]

    client.close()

    return ({"stories deleted": total_stories_deleted}, 200, headers)