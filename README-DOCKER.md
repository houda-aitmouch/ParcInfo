# Configuration Docker pour ParcInfo

Ce document explique la configuration Docker corrigée pour le projet ParcInfo.

## 🚀 Démarrage rapide

```bash
# Démarrer tous les services
./start-docker.sh

# Ou manuellement
docker-compose up --build -d
```

## 📁 Fichiers de configuration

### Variables d'environnement
- `env.docker` : Variables d'environnement pour Docker
- `env.example` : Exemple de configuration pour le développement local

### Dockerfiles
- `Dockerfile.backend` : Backend Django
- `Dockerfile.chatbot` : Service chatbot
- `Dockerfile.frontend` : Frontend React avec Nginx
- `Dockerfile.streamlit` : Dashboard Streamlit

### Scripts
- `start-docker.sh` : Script de démarrage automatisé
- `entrypoint.sh` : Script d'initialisation du backend

## 🔧 Configuration des services

### Base de données PostgreSQL
- **Image** : postgres:15
- **Base** : parcinfo_db
- **Utilisateur** : Houda
- **Mot de passe** : houda123
- **Extensions** : pgvector (pour le chatbot)
- **Healthcheck** : Vérification automatique de la disponibilité

### Backend Django
- **Port** : 8000
- **Settings** : ParcInfo.settings
- **Variables** : Chargées depuis env.docker
- **Dépendances** : Base de données (avec healthcheck)

### Frontend React
- **Port** : 3000
- **Serveur** : Nginx
- **Build** : Vite
- **Fichiers statiques** : Servis par Nginx

### Chatbot
- **Port** : 8001
- **Dépendances** : sentence-transformers, transformers, torch
- **Cache** : Hugging Face models
- **Base de données** : PostgreSQL avec pgvector

### Dashboard Streamlit
- **Port** : 8501
- **Application** : dashboard_garantie.py
- **Configuration** : Variables d'environnement Docker

### Nginx (Reverse Proxy)
- **Port** : 80 (HTTP)
- **Configuration** : nginx.conf
- **Fonction** : Proxy vers les services backend

## 🌐 Accès aux services

| Service | URL | Description |
|---------|-----|-------------|
| Backend | http://localhost:8000 | API Django |
| Frontend | http://localhost:3000 | Interface React |
| Chatbot | http://localhost:8001 | Service chatbot |
| Streamlit | http://localhost:8501 | Dashboard garantie |
| Nginx | http://localhost:80 | Reverse proxy |

## 📋 Commandes utiles

```bash
# Voir les logs
docker-compose logs -f [service]

# Arrêter tous les services
docker-compose down

# Redémarrer un service
docker-compose restart [service]

# Accéder au shell d'un conteneur
docker-compose exec [service] bash

# Reconstruire les images
docker-compose up --build

# Nettoyer les volumes
docker-compose down -v
```

## 🔍 Dépannage

### Problèmes courants

1. **Base de données non accessible**
   ```bash
   # Vérifier le statut
   docker-compose ps
   
   # Voir les logs de la DB
   docker-compose logs db
   ```

2. **Erreurs de migration**
   ```bash
   # Accéder au conteneur backend
   docker-compose exec backend bash
   
   # Exécuter les migrations manuellement
   python manage.py migrate
   ```

3. **Problèmes de fichiers statiques**
   ```bash
   # Collecter les fichiers statiques
   docker-compose exec backend python manage.py collectstatic
   ```

### Logs et monitoring

```bash
# Logs en temps réel
docker-compose logs -f

# Logs d'un service spécifique
docker-compose logs -f backend

# Statut des conteneurs
docker-compose ps

# Utilisation des ressources
docker stats
```

## 🔒 Sécurité

- Les mots de passe sont dans `env.docker` (à changer en production)
- HTTPS désactivé pour le développement
- CORS configuré pour les domaines locaux
- Variables d'environnement sécurisées

## 📝 Notes importantes

1. **Premier démarrage** : Les migrations sont exécutées automatiquement
2. **Cache Hugging Face** : Monté depuis `~/.cache/huggingface`
3. **Fichiers statiques** : Collectés automatiquement au démarrage
4. **Base de données** : pgvector installé automatiquement
5. **Healthchecks** : Vérification de la disponibilité des services

## 🚀 Production

Pour la production, modifiez :
- Les mots de passe dans `env.docker`
- La configuration Nginx pour HTTPS
- Les variables d'environnement sensibles
- La configuration de la base de données
