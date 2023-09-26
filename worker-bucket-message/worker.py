from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Message(BaseModel):
    kind: str
    id: str
    selfLink: str
    name: str
    bucket: str
    generation: str
    metageneration: str
    contentType: str
    timeCreated: str
    updated: str
    storageClass: str
    timeStorageClassUpdated: str
    size: str
    md5Hash: str
    mediaLink: str
    crc32c: str
    etag: str

@app.post('/bucket-message-handler')
async def handle_task(data: Message):
    # Vous pouvez maintenant accéder aux attributs du modèle directement
    # Par exemple:
    print(f"Received message for bucket: {data.bucket}")
    print(f"File name: {data.name}")

    return {"status": "Message processed successfully"}
