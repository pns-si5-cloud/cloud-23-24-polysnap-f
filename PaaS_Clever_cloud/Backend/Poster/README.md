# Backend - PolySnap Post Service

Le service backend Post de PolySnap est responsable de la gestion des messages, des conversations et des stories. Il interagit avec la base de données pour stocker et récupérer les informations nécessaires, et communique également avec d'autres services cloud pour certaines fonctionnalités, comme l'upload de fichiers et la publication dans un Pub/Sub. Vous trouverez ci-dessous une explication des routes fournies par ce service et des interactions associées.

## Routes

Les routes suivantes sont exposées par le service :

- **POST `/conversations/{conversation_id}/messages`** : Ajoute un nouveau message à une conversation.
- **PUT `/conversations/{conversation_id}/messages/{message_id}/read`** : Marque un message comme lu dans une conversation.
- **POST `/conversations`** : Crée une nouvelle conversation.
- **GET `/upload-url`** : Génère une URL signée pour l'upload de fichiers.
- **GET `/users`** : Récupère la liste des utilisateurs.
- **GET `/users/{user_id}`** : Récupère les informations d'un utilisateur spécifique.
- **POST `/stories`** : Crée une nouvelle story.

## Swagger Documentation

La documentation Swagger pour ces routes est accessible à [ce lien](https://app-2921299c-f3f9-4829-b95f-0d2227b41a21.cleverapps.io/docs).

## Responsabilités du Service

- **Gestion des Messages et Conversations** :
  - Le service traite les requêtes du frontend pour envoyer, recevoir et marquer les messages comme lus.
  - Il est responsable de la persistance des données de message dans la base de données.

- **Publication de Messages** :
  - Lorsqu'un message est reçu, il est également publié dans un topic Pub/Sub sur Google Cloud pour une éventuelle consommation par d'autres services.

- **Gestion des Uploads de Fichiers** :
  - Le service génère des URLs signées pour permettre l'upload de fichiers dans un bucket Google Cloud Storage, et renvoie cette URL au frontend pour l'upload direct depuis le client.

- **Gestion des Stories** :
  - Il traite les requêtes pour créer de nouvelles stories et persiste ces informations dans la base de données.

## Interaction avec d'autres Services et Cloud

- **Database** : 
  - Toutes les écritures et lectures de la base de données sont gérées par ce service backend.

- **Google Cloud Pub/Sub** :
  - Publication de messages dans un topic pour une éventuelle consommation par d'autres services.

- **Google Cloud Storage** :
  - Génération d'URLs signées pour l'upload de fichiers.
