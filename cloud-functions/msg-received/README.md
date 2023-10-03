# HTTP Task Creator for Google Cloud Tasks

This module automatically converts messages received via Google Cloud Pub/Sub into HTTP tasks for Google Cloud Tasks.  

When a message is published on a specific Cloud Pub/Sub topic, our function is triggered. This function takes the message, processes it, and creates a corresponding HTTP task in Google Cloud Tasks.