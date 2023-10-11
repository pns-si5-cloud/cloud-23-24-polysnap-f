import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.environ.get("MONGODB_URI")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
COLLECTION_USER = os.environ.get("COLLECTION_USER")
COLLECTION_CONVERSATION = os.environ.get("COLLECTION_CONVERSATION")
