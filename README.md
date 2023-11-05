# PolySnap : Équipe F

## Membres

Nicolas Guiblin | Sylcantor
Chahan Movsessian | Cloud84-blip
Hadil Ayari | HadilAyari00
Floriane Paris | Floriane-PARIS

## Description du projet

PolySnap est une application de messagerie instantanée permettant aux utilisateurs de communiquer efficacement à travers des messages textuels et des médias visuels. Elle propose des fonctionnalités uniques telles que des messages éphémères qui disparaissent après lecture, et la création de groupes de discussion pour une interaction collaborative. En outre, les utilisateurs peuvent partager leur quotidien via des séquences chronologiques de médias appelées PolyStories, visibles temporairement. Grâce à ces fonctionnalités, PolySnap offre une plateforme interactive et sécurisée pour une communication enrichie et authentique.

## Base de code

La base de code est organisée en plusieurs sous-projets distincts, chacun ayant un objectif spécifique dans le fonctionnement global de l'application PolySnap. Ci-dessous, vous trouverez des liens vers les READMEs de chacun de ces sous-projets, où vous pouvez en apprendre davantage sur leur structure, leurs responsabilités et leur fonctionnement.

- [PolySnap Scheduler and Batch Processing](./FaaS_GCP/Batch_with_scheduler/README.md)
- [PolySnap Poster Service](./PaaS_Clever_cloud/Backend/Poster/README.md)
- [Backend - PolySnap Receiver Service](./PaaS_Clever_cloud/Backend/Receiver/README.md)
- [Frontend - PolySnap Interface Utilisateur](./PaaS_Clever_cloud/Frontend/README.md)

## Configuration des déploiements

### Variables d'Environnement

- Définir les variables d'environnement nécessaires sur Clever Cloud et Google Cloud Platform (GCP) pour chaque service.
- Exemple : 
    - `MONGODB_URI`: URI pour la connexion à MongoDB Atlas.
    - `GOOGLE_PROJECT_ID`: Identifiant du projet GCP.

### MongoDB Atlas

- Création d'un cluster sur MongoDB Atlas. (DBaaS)
- Ajout des adresses IP des applications Clever Cloud dans la liste des IP autorisées du cluster MongoDB Atlas.

### Google Cloud Platform (GCP)

- Création d'un compte de service avec les rôles nécessaires pour accéder aux ressources GCP telles que les buckets et Pub/Sub.
- Configuration des Cloud Functions (FaaS) et des Cloud Scheduler (SaaS) pour lancer les batchs la nuit.

### Clever Cloud

- Déploiement des applications sur Clever Cloud. (PaaS)

## Documentation des protocoles de déploiements

### MongoDB Atlas

- [Créer un cluster](https://www.mongodb.com/docs/atlas/tutorial/create-new-cluster/)
- [Accès réseau (IP)](https://www.mongodb.com/docs/atlas/security/ip-access-list/)

### Clever Cloud

- [Déploiement général d'applications](https://www.clever-cloud.com/doc/deploy/application/)
- [Déploiement d'applications Python](https://www.clever-cloud.com/doc/deploy/application/python/python_apps/)
- [Déploiement d'applications Node.js](https://www.clever-cloud.com/doc/deploy/application/javascript/by-framework/nodejs/)
- [Variables d'environnement](https://www.clever-cloud.com/doc/develop/env-variables/)

### Google Cloud Platform (GCP)

- [Déploiement de Cloud Functions](https://cloud.google.com/functions/docs/deploy?hl=fr)
- [Configuration des variables d'environnement pour Cloud Functions](https://cloud.google.com/functions/docs/configuring/env-var?hl=fr)
- [Configuration de Google Scheduler pour exécuter des travaux cron](https://cloud.google.com/scheduler/docs/schedule-run-cron-job?hl=fr)
