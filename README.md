# 🏢 ParcInfo - Gestion de Parc Informatique

## 📋 Vue d'Ensemble

**ParcInfo** est une application web complète de gestion de parc informatique développée avec Django et React. Elle permet la gestion des équipements informatiques et de bureau, des demandes d'équipement, des commandes, des fournisseurs et des livraisons.

## ✨ Fonctionnalités Principales

### 🔧 Gestion des Équipements
- **Matériel Informatique** : Ordinateurs, serveurs, périphériques
- **Matériel de Bureau** : Mobilier, accessoires
- **Suivi d'Inventaire** : Codes d'inventaire, statuts, affectations

### 📝 Gestion des Demandes
- **Demandes d'Équipement** : Création, suivi, approbation
- **Workflow d'Approbation** : Hiérarchie des validations
- **Signatures Électroniques** : Décharges numériques
- **Notifications Automatiques** : Système de notifications en temps réel

### 🛒 Gestion des Commandes
- **Commandes Informatiques** : Matériel informatique
- **Commandes Bureau** : Matériel de bureau
- **Gestion des Fournisseurs** : Catalogue, contacts, devis
- **Suivi des Livraisons** : Statuts, dates, réceptions

### 👥 Gestion des Utilisateurs
- **Rôles et Permissions** : Employé, Gestionnaire, Super Admin
- **Profils Personnalisés** : Informations, équipements affectés
- **Authentification Sécurisée** : Login/logout, sessions

### 🤖 Chatbot Intelligent
- **Assistant IA** : Réponses automatiques aux questions
- **Base de Connaissances** : Documentation intégrée
- **Recherche Sémantique** : RAG (Retrieval-Augmented Generation)

## 🏗️ Architecture Technique

### Backend (Django)
```
ParcInfo/
├── apps/
│   ├── users/                 # Gestion des utilisateurs
│   ├── demande_equipement/    # Demandes d'équipement
│   ├── materiel_informatique/ # Matériel informatique
│   ├── materiel_bureautique/  # Matériel de bureau
│   ├── commande_informatique/ # Commandes informatiques
│   ├── commande_bureau/       # Commandes bureau
│   ├── fournisseurs/          # Gestion des fournisseurs
│   ├── livraison/             # Suivi des livraisons
│   └── chatbot/               # Assistant IA
├── ParcInfo/                  # Configuration Django
├── templates/                 # Templates HTML
├── static/                    # Fichiers statiques
└── media/                     # Fichiers uploadés
```

### Frontend (React + TypeScript)
```
frontend/
├── components/                # Composants React
├── contexts/                  # Contextes React
├── styles/                    # Styles CSS
└── assets/                    # Ressources
```

## 🚀 Installation et Configuration

### Prérequis
- Python 3.8+
- Node.js 16+
- PostgreSQL (recommandé) ou SQLite
- Docker (optionnel)

### Installation Rapide

1. **Cloner le projet**
```bash
git clone https://github.com/votre-repo/parcinfo.git
cd parcinfo
```

2. **Installation Backend**
```bash
# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configuration de la base de données
python manage.py makemigrations
python manage.py migrate

# Créer un super utilisateur
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver
```

3. **Installation Frontend**
```bash
cd frontend
npm install
npm run dev
```

## 🐳 Déploiement Docker

### Images Docker Disponibles
- `parcinfo-backend:latest` (6.67 GB) - Backend Django complet
- `parcinfo-chatbot:latest` (6.67 GB) - Chatbot IA intégré
- `parcinfo-frontend:latest` (81.41 MB) - Frontend React optimisé
- `postgres:15` (650.26 MB) - Base de données PostgreSQL
- `nginx:alpine` (80.2 MB) - Serveur web Nginx

### Démarrage Rapide
```bash
# Démarrer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter les services
docker-compose down
```

### Scripts Utiles
```bash
# Script de déploiement
./deploy.sh

# Sauvegarde des images
./save-images.sh

# Restauration des images
./restore-images.sh
```

## ☁️ Déploiement Cloud

### Azure (Recommandé)
- Guide complet : `AZURE_DEPLOYMENT.md`
- Coût estimé : ~$20-30/mois
- Crédit Azure for Students : $100

### Railway
- Guide : `RAILWAY_OPTIMIZED_DEPLOYMENT.md`
- Gratuit : 5$ de crédit/mois
- Image optimisée < 4GB

## 🔧 Configuration

### Variables d'Environnement
Créer un fichier `.env` :
```env
# Django
SECRET_KEY=votre-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de données
DATABASE_URL=postgresql://user:password@localhost/parcinfo

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe

# Chatbot IA
OPENAI_API_KEY=votre-clé-api-openai
```

## 🌐 URLs d'Accès

### Local
- **Application** : http://localhost:8000
- **Admin Django** : http://localhost:8000/admin/
- **Frontend** : http://localhost:3000

### Production
- **Application** : https://votre-domaine.com
- **Admin Django** : https://votre-domaine.com/admin/

## 🔐 Identifiants par Défaut

### Super Utilisateur Django
- **Username** : admin
- **Email** : admin@parcinfo.com
- **Password** : admin123

## 📊 Monitoring

### Logs
```bash
# Logs en temps réel
docker-compose logs -f

# Logs spécifiques
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Statut des Services
```bash
# Liste des conteneurs
docker-compose ps

# Ressources utilisées
docker stats
```

## 🛠️ Maintenance

### Sauvegarde
```bash
# Sauvegarder la base de données
docker-compose exec db pg_dump -U parcinfo_user parcinfo > backup.sql

# Restaurer
docker-compose exec -T db psql -U parcinfo_user parcinfo < backup.sql
```

### Mise à Jour
```bash
# Reconstruire les images
docker-compose build --no-cache

# Redémarrer les services
docker-compose up -d --force-recreate
```

## 🎯 Pour votre Soutenance

### Démonstration Live
1. **Démarrage rapide** : `docker-compose up -d`
2. **Accès à l'application** : http://localhost:8000
3. **Fonctionnalités** : Dashboard, demandes, chatbot
4. **Admin** : http://localhost:8000/admin/

### Points Techniques
- ✅ **Architecture Docker** : Microservices
- ✅ **Base de données** : PostgreSQL
- ✅ **Frontend moderne** : React + TypeScript
- ✅ **IA intégrée** : Chatbot intelligent
- ✅ **Déploiement cloud** : Azure/Railway ready
- ✅ **Monitoring** : Logs et métriques

## 📄 Licence

Ce projet est sous licence MIT.

## 👥 Support

- **Email** : support@parcinfo.com
- **Documentation** : Voir les fichiers .md du projet
- **Issues** : GitHub Issues

---

**🎉 ParcInfo - Gestion intelligente de votre parc informatique !**