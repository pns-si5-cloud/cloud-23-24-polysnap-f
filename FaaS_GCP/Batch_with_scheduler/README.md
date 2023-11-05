# PolySnap Scheduler and Batch Processing

Ce service est destiné à nettoyer les données expirées de la base de données. Il comprend deux tâches principales qui sont exécutées en batch pour garantir l'efficacité et la performance lors de la manipulation d'un grand volume de données.

## Scripts

### `delete_messages_expired.py`

Ce script est conçu pour parcourir la collection de conversations dans la base de données, identifier les messages qui sont marqués comme 'smoke' et qui sont expirés, puis les supprimer de la base de données.

- **Fonctions Principales** :
    - `cleanup_batch` : Parcourt les conversations en batch, identifie et collecte les IDs des messages expirés.
    - `schedule_cleanup` : Gère les requêtes HTTP, initialise la connexion à la base de données, et orchestre l'exécution des batchs de nettoyage.

### `delete_stories_expired.py`

Ce script est conçu pour parcourir la collection de stories dans la base de données, identifier les stories qui sont expirées, puis les supprimer de la base de données et des profils des utilisateurs.

- **Fonctions Principales** :
    - `cleanup_batch` : Parcourt les stories en batch, identifie et collecte les IDs des stories expirées.
    - `schedule_cleanup` : Gère les requêtes HTTP, initialise la connexion à la base de données, et orchestre l'exécution des batchs de nettoyage.

## Scheduler GCP

Deux schedulers GCP sont configurés pour envoyer des requêtes HTTP afin de déclencher les scripts :

- Le scheduler pour `delete_messages_expired.py` est programmé pour s'exécuter à 4h du matin.
- Le scheduler pour `delete_stories_expired.py` est programmé pour s'exécuter à 5h du matin.
