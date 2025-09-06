# 🐳 Images Docker ParcInfo - Prêtes pour le Déploiement

## 📋 Images Disponibles (5 images optimisées)

### **Images Principales**
| Image | Taille | Description | Usage |
|-------|--------|-------------|-------|
| `parcinfo-backend:latest` | 6.67 GB | Backend Django complet | Déploiement principal |
| `parcinfo-chatbot:latest` | 6.67 GB | Chatbot IA intégré | Service IA |
| `parcinfo-frontend:latest` | 81.41 MB | Frontend React optimisé | Interface utilisateur |

### **Images de Support**
| Image | Taille | Description | Usage |
|-------|--------|-------------|-------|
| `postgres:15` | 650.26 MB | Base de données PostgreSQL | Base de données |
| `nginx:alpine` | 80.2 MB | Serveur web Nginx | Reverse proxy |

### **Total des images** : ~14.1 GB

## 🚀 Commandes de Déploiement

### **1. Démarrage Local avec Docker Compose**
```bash
# Démarrer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter les services
docker-compose down
```

### **2. Déploiement Azure**
```bash
# Construire l'image Azure
docker build -f Dockerfile.azure -t parcinfo-azure .

# Taguer pour Azure Container Registry
docker tag parcinfo-azure parcinforegistry.azurecr.io/parcinfo:latest

# Pousser vers Azure
docker push parcinforegistry.azurecr.io/parcinfo:latest
```

### **3. Déploiement Railway**
```bash
# Utiliser l'image ultra-optimisée
docker build -f Dockerfile.railway.ultra-optimized -t parcinfo-railway .

# Taguer pour Railway
docker tag parcinfo-railway railway.app/parcinfo:latest
```

## 🔧 Configuration des Services

### **Backend (parcinfo-backend)**
- **Port** : 8000
- **Variables d'environnement** :
  - `DATABASE_URL` : URL de la base de données
  - `SECRET_KEY` : Clé secrète Django
  - `DEBUG` : Mode debug (False en production)
  - `ALLOWED_HOSTS` : Hosts autorisés

### **Frontend (parcinfo-frontend)**
- **Port** : 3000
- **Build** : Production optimisée
- **Assets** : Statiques collectés

### **Chatbot (parcinfo-chatbot)**
- **Port** : 8001
- **IA** : Modèles BART et sentence-transformers
- **RAG** : Recherche augmentée par récupération

### **PostgreSQL (postgres:15)**
- **Port** : 5432
- **Base** : parcinfo
- **Utilisateur** : parcinfo_user
- **Mot de passe** : parcinfo_password

## 📊 Optimisations Appliquées

### **Backend (6.68 GB)**
- ✅ **Python 3.11-slim** : Image de base légère
- ✅ **Django 5.2.4** : Framework web optimisé
- ✅ **Gunicorn** : Serveur WSGI performant
- ✅ **Whitenoise** : Servir les fichiers statiques
- ✅ **PostgreSQL** : Driver optimisé
- ✅ **IA intégrée** : Chatbot et RAG

### **Frontend (81.4 MB)**
- ✅ **React 18** : Interface moderne
- ✅ **TypeScript** : Typage statique
- ✅ **Tailwind CSS** : Styles utilitaires
- ✅ **Vite** : Build tool rapide
- ✅ **Production build** : Optimisé et minifié

### **Chatbot (6.68 GB)**
- ✅ **BART-large-mnli** : Modèle de classification
- ✅ **sentence-transformers** : Embeddings
- ✅ **RAG** : Recherche sémantique
- ✅ **API REST** : Interface standardisée

## 🌐 URLs d'Accès

### **Local (Docker Compose)**
- **Application** : http://localhost:8000
- **Admin Django** : http://localhost:8000/admin/
- **Frontend** : http://localhost:3000
- **Chatbot API** : http://localhost:8001

### **Production (Azure/Railway)**
- **Application** : https://votre-domaine.com
- **Admin Django** : https://votre-domaine.com/admin/
- **API** : https://votre-domaine.com/api/

## 🔐 Identifiants par Défaut

### **Super Utilisateur Django**
- **Username** : admin
- **Email** : admin@parcinfo.com
- **Password** : admin123

### **Base de Données**
- **Host** : localhost (local) / votre-host (production)
- **Port** : 5432
- **Database** : parcinfo
- **Username** : parcinfo_user
- **Password** : parcinfo_password

## 📈 Monitoring et Logs

### **Voir les logs en temps réel**
```bash
# Tous les services
docker-compose logs -f

# Service spécifique
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f chatbot
```

### **Statut des conteneurs**
```bash
# Liste des conteneurs
docker-compose ps

# Ressources utilisées
docker stats
```

## 🛠️ Maintenance

### **Mise à jour des images**
```bash
# Reconstruire les images
docker-compose build --no-cache

# Redémarrer les services
docker-compose up -d --force-recreate
```

### **Sauvegarde de la base de données**
```bash
# Sauvegarder
docker-compose exec db pg_dump -U parcinfo_user parcinfo > backup.sql

# Restaurer
docker-compose exec -T db psql -U parcinfo_user parcinfo < backup.sql
```

## 🎯 Pour votre Soutenance

### **Démonstration Live**
1. **Démarrage rapide** : `docker-compose up -d`
2. **Accès à l'application** : http://localhost:8000
3. **Fonctionnalités** : Dashboard, demandes, chatbot
4. **Admin** : http://localhost:8000/admin/

### **Points Techniques**
- ✅ **Architecture Docker** : Microservices
- ✅ **Base de données** : PostgreSQL
- ✅ **Frontend moderne** : React + TypeScript
- ✅ **IA intégrée** : Chatbot intelligent
- ✅ **Déploiement cloud** : Azure/Railway ready
- ✅ **Monitoring** : Logs et métriques

---

**🎉 Votre projet ParcInfo est prêt pour le déploiement professionnel !**
