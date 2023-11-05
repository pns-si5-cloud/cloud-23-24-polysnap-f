import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.environ.get("MONGODB_URI")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
COLLECTION_USER = os.environ.get("COLLECTION_USER")
COLLECTION_CONVERSATION = os.environ.get("COLLECTION_CONVERSATION")
COLLECTION_STORY = os.environ.get("COLLECTION_STORY")
GOOGLE_APPLICATION_CREDENTIALS_CONTENT = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_CONTENT")
BUCKET_NAME = os.environ.get("BUCKET_NAME")
CLOUD_GENERATOR_URL = os.environ.get("CLOUD_GENERATOR_URL")
GOOGLE_PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID")
GOOGLE_TOPIC_ID = os.environ.get("GOOGLE_TOPIC_ID")
