# Créateur de Tâches HTTP pour Google Cloud Task

Ce module permet de transformer automatiquement les messages reçus via Google Cloud Pub/Sub en tâches HTTP pour Google Cloud Tasks.  

Lorsqu'un message est publié sur un sujet spécifique de Cloud Pub/Sub, notre fonction est déclenchée. Cette fonction prend le message, le traite, et crée une tâche HTTP correspondante dans Google Cloud Tasks  