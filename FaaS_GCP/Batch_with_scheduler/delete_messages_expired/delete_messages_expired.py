from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import UpdateOne
from datetime import datetime, timedelta
import asyncio
import os
from dotenv import load_dotenv
import functions_framework

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_CONVERSATION = os.getenv("COLLECTION_CONVERSATION")

async def cleanup_batch(collection, batch_size, skip):
    # Initialisation de la liste qui va contenir les IDs des conversations mises à jour
    conversations_updated = []
    update_operations = []  # Liste pour contenir les opérations de mise à jour
    update_required = False  # Indicateur pour vérifier si des mises à jour sont nécessaires

    # Récupération et traitement par lot des conversations
    async for conversation in collection.find().skip(skip).limit(batch_size):
        messages_to_remove = []
        current_utc_time = datetime.utcnow()

        for message in conversation['messages']:
            if message['smoke'] == True:
                read_by_all = all(participant in message['read_by'] for participant in conversation['participants'])
                message_time = datetime.fromisoformat(message['timestamp'])
                expiration_time = message_time + timedelta(minutes=conversation['read_duration'])

                if read_by_all and current_utc_time > expiration_time:
                    messages_to_remove.append(message['_id'])

        if messages_to_remove:
            update_operations.append(
                UpdateOne({"_id": conversation['_id']}, {"$pull": {"messages": {"_id": {"$in": messages_to_remove}}}})
            )
            conversations_updated.append(str(conversation['_id']))
            update_required = True

    # Exécutez les opérations en bloc si nécessaire
    if update_required:
        await collection.bulk_write(update_operations)

    return conversations_updated

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
    conversations_collection = db[COLLECTION_CONVERSATION]

    batch_size = 10000  # Nombre de conversations par lot
    # Calculez le nombre de lots nécessaires pour couvrir toutes les conversations
    total_conversations = await conversations_collection.count_documents({})
    num_batches = (total_conversations + batch_size - 1) // batch_size

    total_conversations_updated = []

    # Créez des tâches de nettoyage par lots
    tasks = [
        cleanup_batch(conversations_collection, batch_size, i * batch_size)
        for i in range(num_batches)
    ]

    # Exécutez les tâches en parallèle et collectez les résultats
    results = await asyncio.gather(*tasks)

    # Agrégez les IDs des conversations mises à jour
    for batch_result in results:
        total_conversations_updated.extend(batch_result)

    client.close()

    return ({"conversations_updated": total_conversations_updated}, 200, headers)