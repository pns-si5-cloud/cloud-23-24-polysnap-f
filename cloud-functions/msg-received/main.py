import base64
import json
import os
from google.cloud import tasks_v2
from google.protobuf import duration_pb2, timestamp_pb2
import functions_framework
import datetime
from typing import Dict, Optional

PROJECT_ID = os.environ.get('GOOGLE_CLOUD_PROJECT', 'cloud-project-399418')
LOCATION = os.environ.get('REGION', 'europe-west1')
QUEUE_NAME = os.environ.get('GOOGLE_TASK','bucket-message-queue1')
SERVICE_URL = os.environ.get('WORKER_URL','https://worker-bucket-message-dot-cloud-project-399418.ew.r.appspot.com')
URL = SERVICE_URL + '/bucket-message-handler'

def create_http_task(
    project: str,
    location: str,
    queue: str,
    url: str,
    json_payload: Dict,
    scheduled_seconds_from_now: Optional[int] = None,
    task_id: Optional[str] = None,
    deadline_in_seconds: Optional[int] = None,
) -> tasks_v2.Task:
    """Create an HTTP POST task with a JSON payload.
    Args:
        project: The project ID where the queue is located.
        location: The location where the queue is located.
        queue: The ID of the queue to add the task to.
        url: The target URL of the task.
        json_payload: The JSON payload to send.
        scheduled_seconds_from_now: Seconds from now to schedule the task for.
        task_id: ID to use for the newly created task.
        deadline_in_seconds: The deadline in seconds for task.
    Returns:
        The newly created task.
    """

    # Create a client.
    client = tasks_v2.CloudTasksClient()

    # Construct the task.
    task = tasks_v2.Task(
        http_request=tasks_v2.HttpRequest(
            http_method=tasks_v2.HttpMethod.POST,
            url=url,
            headers={"Content-type": "application/json"},
            body=json.dumps(json_payload).encode(),
        ),
        name=(
            client.task_path(project, location, queue, task_id)
            if task_id is not None
            else None
        ),
    )

    # Convert "seconds from now" to an absolute Protobuf Timestamp
    if scheduled_seconds_from_now is not None:
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(
            datetime.datetime.utcnow()
            + datetime.timedelta(seconds=scheduled_seconds_from_now)
        )
        task.schedule_time = timestamp

    # Convert "deadline in seconds" to a Protobuf Duration
    if deadline_in_seconds is not None:
        duration = duration_pb2.Duration()
        duration.FromSeconds(deadline_in_seconds)
        task.dispatch_deadline = duration

    # Use the client to send a CreateTaskRequest.
    return client.create_task(
        tasks_v2.CreateTaskRequest(
            # The queue to add the task to
            parent=client.queue_path(project, location, queue),
            # The task itself
            task=task,
        )
    )

@functions_framework.cloud_event
def bucket_to_task(cloud_event):
    """Triggered by a message on a Cloud Pub/Sub topic."""
    
    # Décodage du message Pub/Sub
    pubsub_message = base64.b64decode(cloud_event.data["message"]["data"])

    print(f"pubsub_message: {pubsub_message}")
    
    # Convertir le message en JSON (si nécessaire)
    payload = json.loads(pubsub_message)

    print(f"payload : {payload}")

    # Appeler la fonction pour créer la tâche
    task = create_http_task(PROJECT_ID, LOCATION, QUEUE_NAME, URL, payload)

    print(f"Task {task.name} created")


