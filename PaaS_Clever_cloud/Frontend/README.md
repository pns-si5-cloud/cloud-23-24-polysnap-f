# Frontend - PolySnap Interface Utilisateur

L'interface utilisateur de PolySnap est principalement chargée de fournir une interface pour les utilisateurs, permettant des interactions avec le système. Elle joue également un rôle crucial dans la gestion de l'état des données, des communications en temps réel avec le backend via WebSocket, et des interactions avec les différentes fonctionnalités fournies par PolySnap. Voici une description détaillée des composants, des responsabilités et des interactions avec le service backend.

## Composants

Les composants suivants font partie de l'interface utilisateur de PolySnap :

- **Conversations** :
  - Permet aux utilisateurs de voir leurs conversations existantes et d'en démarrer de nouvelles.
  - Affiche les messages au sein d'une conversation et permet l'envoi de nouveaux messages.

- **Stories** :
  - Permet aux utilisateurs de créer et de voir des stories.

- **Upload de fichiers** :
  - Permet aux utilisateurs d'uploader des images qui peuvent être partagés dans des messages ou des stories.

- **Profil Utilisateur** :
  - Affiche les informations du profil d'un utilisateur et permet la mise à jour de ces informations.

- **Recherche d'Utilisateurs** :
  - Permet la recherche d'autres utilisateurs et l'initiation de nouvelles conversations.

## Interaction avec le Backend

- **API Requests** :
  - Toutes les requêtes nécessaires pour récupérer ou envoyer des données sont faites au service backend de PolySnap.

- **WebSocket Communication** :
  - Une communication en temps réel est établie avec le backend pour la réception instantanée des messages et des notifications.

## Responsabilités du Frontend

- **Gestion de l'État** :
  - Le frontend gère l'état des données utilisateur, des conversations, des messages et des stories, ce qui inclut la conservation des données, la mise à jour de l'état, le rendu réactif, la communication avec le backend, la gestion des erreurs et des états de chargement, et le cache local.

- **Rendu de l'UI** :
  - Le frontend est responsable du rendu de l'interface utilisateur et de la présentation des données aux utilisateurs.

- **Gestion des Notifications** :
  - Il est également responsable de la gestion des notifications et des alertes utilisateur.

- **Validation du Client** :
  - Validation des entrées utilisateur et gestion des erreurs.
