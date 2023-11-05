import json
import datetime
from uuid import uuid1
from google.cloud import storage
from google.oauth2 import service_account

from config import GOOGLE_APPLICATION_CREDENTIALS_CONTENT

def get_storage_client_from_env():
    credentials_json = GOOGLE_APPLICATION_CREDENTIALS_CONTENT
    credentials_info = json.loads(credentials_json)
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
    
    return storage.Client(credentials=credentials)

def generate_upload_signed_url_v4(bucket_name: str, content_type: str):
    
    """Generates a v4 signed URL for uploading a blob using HTTP PUT.

    Note that this method requires a service account key file. You can not use
    this if you are using Application Default Credentials from Google Compute
    Engine or from the Google Cloud SDK.
    """
    blob_name = uuid1().hex

    storage_client = get_storage_client_from_env()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta(minutes=15),
        # Allow PUT requests using this URL.
        method="PUT",
        content_type=content_type,
    )
    
    return blob_name, url