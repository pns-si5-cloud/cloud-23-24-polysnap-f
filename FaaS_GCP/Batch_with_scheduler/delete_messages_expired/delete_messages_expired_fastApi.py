from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import UpdateOne
from datetime import datetime, timedelta
import asyncio
import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_CONVERSATION = os.getenv("COLLECTION_CONVERSATION")

@app.on_event("startup")
async def startup_db_client():
    app.client = AsyncIOMotorClient(MONGODB_URI)
    app.db = app.client[DATABASE_NAME]
    app.conversations_collection = app.db[COLLECTION_CONVERSATION]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.client.close()

async def cleanup_batch(collection, batch_size, skip):
    # Initialisation de la liste qui va contenir les IDs des conversations mises à jour
    conversations_updated = []
    update_operations = []  # Liste pour contenir les opérations de mise à jour
    update_required = False  # Indicateur pour vérifier si des mises à jour sont nécessaires

    # Récupération et traitement par lot des conversations
    async for conversation in collection.find().skip(skip).limit(batch_size):
        print(conversation)

        messages_to_remove = []
        current_utc_time = datetime.utcnow()

        for message in conversation['messages']:
            read_by_all = all(participant in message['read_by'] for participant in conversation['participants'])

            message_time = datetime.fromisoformat(message['timestamp'])
            print("message_time")
            print(message_time)
            expiration_time = message_time + timedelta(minutes=conversation['read_duration'])
            print("current_utc_time")   
            print(current_utc_time)
            print("expiration_time")
            print(expiration_time)
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

@app.put("/cleanup-messages/")
async def schedule_cleanup():
    batch_size = 10000  # Nombre de conversations par lot
    # Calculez le nombre de lots nécessaires pour couvrir toutes les conversations
    total_conversations = await app.conversations_collection.count_documents({})
    num_batches = (total_conversations + batch_size - 1) // batch_size

    total_conversations_updated = []

    # Créez des tâches de nettoyage par lots
    tasks = [
        cleanup_batch(app.conversations_collection, batch_size, i * batch_size)
        for i in range(num_batches)
    ]

    # Exécutez les tâches en parallèle et collectez les résultats
    results = await asyncio.gather(*tasks)

    # Agrégez les IDs des conversations mises à jour
    for batch_result in results:
        total_conversations_updated.extend(batch_result)

    return {"conversations_updated": total_conversations_updated}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010)
