# Backend - PolySnap Receiver Service

Le service backend Receiver de PolySnap est principalement chargé de la réception, du traitement des messages et de l'interaction avec la base de données pour la récupération des informations. Il joue également un rôle crucial dans la gestion des communications en temps réel avec les utilisateurs via WebSocket. Voici une description détaillée des routes, des responsabilités et des interactions avec d'autres services et systèmes cloud.

## Routes

Les routes suivantes sont exposées par ce service :

- **POST `/server/message`** : Reçoit un message et le traite en conséquence.
- **GET `/server/history`** : Récupère l'historique des conversations.
- **GET `/server/conversation/:id/history`** : Récupère l'historique d'une conversation spécifique.
- **GET `/server/conversation/:id`** : Récupère les détails d'une conversation spécifique.
- **GET `/server/users/:userId/stories/viewable`** : Récupère les stories visibles par un utilisateur spécifique.

## Documentation Swagger

La documentation Swagger pour ces routes est accessible à [ce lien](https://app-7b3a3c98-565a-4b75-9e80-683f4e59b229.cleverapps.io/api).

## Responsabilités du Service

- **Réception des Messages** :
  - Le service est abonné au topic Pub/Sub sur Google Cloud et reçoit des messages qui sont ensuite traités et envoyés aux utilisateurs concernés via WebSocket.
  
- **Gestion des Conversations et Historique** :
  - Le service fournit des endpoints pour récupérer les détails des conversations ainsi que leur historique.
  
- **Gestion des Stories** :
  - Il fournit également un endpoint pour récupérer les stories visibles par un utilisateur spécifique.

- **Interaction avec WebSocket** :
  - Le service utilise WebSocket pour transmettre les messages en temps réel aux utilisateurs concernés.

## Interaction avec d'autres Services et Cloud

- **Database** : 
  - Toutes les lectures de la base de données sont gérées par ce service backend.
  
- **Google Cloud Pub/Sub** :
  - Abonnement à un topic pour recevoir des messages qui seront ensuite transmis aux utilisateurs via WebSocket.

Pour plus de détails sur la configuration et les protocoles de déploiement, veuillez vous référer aux sections correspondantes de la documentation principale.

