"""Publishes multiple messages to a Pub/Sub topic with an error handler."""
import json
from concurrent import futures
from google.cloud import pubsub_v1
from typing import Callable
from config import GOOGLE_PROJECT_ID, GOOGLE_APPLICATION_CREDENTIALS_CONTENT
from google.oauth2 import service_account

def get_publisher_client_from_env():
    credentials_json = GOOGLE_APPLICATION_CREDENTIALS_CONTENT
    credentials_info = json.loads(credentials_json)
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
    return pubsub_v1.PublisherClient(credentials=credentials)

def get_callback(publish_future, data):
    def callback(publish_future):
        try:
            # Attendez 60 secondes pour que l'appel de publication réussisse.
            print(publish_future.result(timeout=60))
        except futures.TimeoutError:
            print(f"Publication de {data} a expiré.")
    return callback

def publish_message_to_topic(data: str, topic_id: str) -> futures.Future:
    """
    Publie le message sur le topic Google Cloud Pub/Sub.
    """
    print("Publishing message to topic")
    publisher = get_publisher_client_from_env()
    project_id = GOOGLE_PROJECT_ID
    data = json.dumps(data)

    topic_path = publisher.topic_path(project_id, topic_id)
    # Lorsque vous publiez un message, le client retourne un futur.
    publish_future = publisher.publish(topic_path, data.encode("utf-8"))
    # Non-blocking. Les échecs de publication sont gérés dans la fonction de rappel.
    publish_future.add_done_callback(get_callback(publish_future, data))
    # Pour cet exemple, nous attendons que le message soit publié avant de continuer.
    # Dans un scénario réel, en fonction de vos besoins, vous pourriez décider de ne pas attendre.
    future = futures.wait([publish_future], return_when=futures.ALL_COMPLETED)
    return future