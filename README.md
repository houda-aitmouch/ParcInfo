# 🏢 ParcInfo - Gestion de Parc Informatique

## 📋 Vue d'Ensemble

**ParcInfo** est une application web complète de gestion de parc informatique développée avec Django, React et Streamlit. Elle utilise une architecture hybride Kubernetes + Docker pour une performance optimale et une scalabilité maximale.

## ✨ Fonctionnalités Principales

### 🔧 Gestion des Équipements
- **Matériel Informatique** : Ordinateurs, serveurs, périphériques
- **Matériel de Bureau** : Mobilier, accessoires
- **Suivi d'Inventaire** : Codes d'inventaire, statuts, affectations
- **Décharges Numériques** : Signatures électroniques avec PDF

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
- **Modèles Hugging Face** : sentence-transformers pour l'IA

### 📊 Dashboard de Garanties
- **Interface Streamlit** : Dashboard interactif et moderne
- **Visualisations** : Graphiques et métriques en temps réel
- **Gestion des Garanties** : Suivi et alertes automatiques

## 🏗️ Architecture Technique

### Solution Hybride Kubernetes + Docker

```
┌─────────────────────────────────────────────────────────────┐
│                    SOLUTION HYBRIDE                        │
├─────────────────────────────────────────────────────────────┤
│  KUBERNETES (Services principaux)                          │
│  ├── Backend Django    : Port 8000                         │
│  ├── Frontend React    : Port 3000                         │
│  └── Streamlit Dashboard: Port 8501                        │
│                                                             │
│  DOCKER (Chatbot stable)                                   │
│  └── Chatbot AI       : Port 8001                          │
│                                                             │
│  BASE DE DONNÉES                                           │
│  └── PostgreSQL       : Port 5432 (partagée)              │
└─────────────────────────────────────────────────────────────┘
```

### Structure du Projet

```
ParcInfo/
├── apps/                           # Applications Django
│   ├── users/                      # Gestion des utilisateurs
│   ├── demande_equipement/         # Demandes d'équipement
│   ├── materiel_informatique/      # Matériel informatique
│   ├── materiel_bureautique/       # Matériel de bureau
│   ├── commande_informatique/      # Commandes informatiques
│   ├── commande_bureau/            # Commandes bureau
│   ├── fournisseurs/               # Gestion des fournisseurs
│   ├── livraison/                  # Suivi des livraisons
│   └── chatbot/                    # Assistant IA
├── dashboard_garantie/             # Dashboard Streamlit
│   ├── dashboard_garantie.py       # Application principale
│   └── custom_styles.css           # Styles personnalisés
├── frontend/                       # Application React
│   ├── components/                 # Composants React
│   ├── contexts/                   # Contextes React
│   └── styles/                     # Styles CSS
├── k8s/                           # Configuration Kubernetes
│   ├── backend.yaml               # Déploiement Backend
│   ├── frontend.yaml              # Déploiement Frontend
│   ├── streamlit.yaml             # Déploiement Streamlit
│   ├── chatbot.yaml               # Déploiement Chatbot
│   └── configmap.yaml             # Configuration
├── ParcInfo/                      # Configuration Django
├── templates/                     # Templates HTML
├── static/                        # Fichiers statiques
└── media/                         # Fichiers uploadés
```

## 🚀 Installation et Configuration

### Prérequis
- Python 3.8+
- Node.js 16+
- PostgreSQL
- Docker & Docker Compose
- Kubernetes (Docker Desktop ou Minikube)
- kubectl

### Installation Rapide

1. **Cloner le projet**
```bash
git clone https://github.com/houda-aitmouch/ParcInfo.git
cd ParcInfo
```

2. **Déploiement de la Solution Hybride**
```bash
# Déploiement automatique complet
./deploy_hybrid_solution.sh

# Ou déploiement manuel
# 1. Démarrer PostgreSQL
docker-compose up -d postgres

# 2. Démarrer le chatbot Docker
docker-compose up -d chatbot

# 3. Déployer les services Kubernetes
kubectl apply -f k8s/
```

3. **Vérification du déploiement**
```bash
# Vérifier les pods Kubernetes
kubectl get pods -n parcinfo

# Vérifier les services Docker
docker-compose ps

# Tester l'application
./test_final_hybrid.py
```

## 🌐 URLs d'Accès

### Services Kubernetes
- **Backend Django** : http://localhost:8000
- **Frontend React** : http://localhost:3000
- **Streamlit Dashboard** : http://localhost:8501

### Services Docker
- **Chatbot IA** : http://localhost:8001/chatbot/

### Accès via Port-Forward
```bash
# Backend
kubectl port-forward -n parcinfo service/backend-service 8000:8000

# Frontend
kubectl port-forward -n parcinfo service/frontend-service 3000:3000

# Streamlit
kubectl port-forward -n parcinfo service/streamlit-service 8501:8501
```

## 🔐 Identifiants par Défaut

### Super Utilisateur Django
- **Username** : superadmin
- **Email** : admin@parcinfo.com
- **Password** : admin123

### Utilisateurs de Test
- **Employé** : employe / employe123
- **Gestionnaire Info** : gestionnaire_info / gestionnaire123
- **Gestionnaire Bureau** : gestionnaire_bureau / gestionnaire123

## 🧪 Tests et Validation

### Scripts de Test Disponibles
```bash
# Test complet de la solution hybride
python test_final_hybrid.py

# Test des workflows GitHub Actions
python test_github_actions.py

# Test de redirection Dashboard Garantie
python test_dashboard_redirect.py

# Test du chatbot
python test_final_docker_chatbot.py
```

### Tests GitHub Actions
- ✅ Configuration Django validée
- ✅ Imports et dépendances vérifiés
- ✅ Fichiers Docker et Kubernetes validés
- ✅ Tests sans base de données (SQLite en mémoire)

## 🐳 Configuration Docker

### Images Docker
- `parcinfo-backend:latest` - Backend Django
- `parcinfo-chatbot:latest` - Chatbot IA avec modèles Hugging Face
- `parcinfo-frontend:latest` - Frontend React
- `parcinfo-streamlit:latest` - Dashboard Streamlit
- `postgres:15` - Base de données PostgreSQL

### Variables d'Environnement
```env
# Django
SECRET_KEY=votre-secret-key
DEBUG=True
ALLOWED_HOSTS=*

# Base de données
DB_HOST=host.docker.internal
DB_NAME=parcinfo_db
DB_USER=Houda
DB_PASSWORD=

# Chatbot IA
TRANSFORMERS_CACHE=/root/.cache/huggingface
HF_HOME=/root/.cache/huggingface
HF_DISABLE_PROGRESS_BARS=1
```

## ☸️ Configuration Kubernetes

### Namespace
```bash
kubectl create namespace parcinfo
```

### Services NodePort
- Backend : Port 30080
- Frontend : Port 30081
- Streamlit : Port 30085
- Chatbot : Port 30086

### Volumes Persistants
- Cache Hugging Face : `/Users/HouDa/PycharmProjects/docker_model_cache`
- Base de données : Volume PostgreSQL

## 🔧 Maintenance et Monitoring

### Logs
```bash
# Logs Kubernetes
kubectl logs -n parcinfo deployment/backend
kubectl logs -n parcinfo deployment/streamlit

# Logs Docker
docker-compose logs -f chatbot
```

### Redémarrage des Services
```bash
# Redémarrer un pod Kubernetes
kubectl rollout restart deployment/backend -n parcinfo

# Redémarrer le chatbot Docker
docker-compose restart chatbot
```

### Sauvegarde
```bash
# Sauvegarder la base de données
docker-compose exec postgres pg_dump -U Houda parcinfo_db > backup.sql

# Sauvegarder le cache des modèles IA
tar -czf huggingface_cache_backup.tar.gz /Users/HouDa/PycharmProjects/docker_model_cache
```

## 🎯 Fonctionnalités Avancées

### Dashboard de Garanties
- **Interface Streamlit** : Dashboard moderne et interactif
- **CSS Personnalisé** : Styles adaptés au design
- **Redirection Automatique** : Depuis le backend Django
- **Authentification** : Intégration avec le système d'utilisateurs

### Chatbot Intelligent
- **Modèles Hugging Face** : sentence-transformers
- **Cache Persistant** : Évite les téléchargements répétés
- **API REST** : Intégration avec le frontend
- **Base de Connaissances** : Documentation du projet

### Gestion des Décharges
- **PDF Automatiques** : Génération avec logo et signatures
- **Signatures Électroniques** : Canvas HTML5
- **Archivage** : Stockage organisé par date
- **Notifications** : Alertes automatiques

## 🚀 Déploiement en Production

### Script de Déploiement
```bash
# Déploiement complet
./deploy_hybrid_solution.sh

# Vérification
kubectl get all -n parcinfo
docker-compose ps
```

### Monitoring
```bash
# Statut des services
kubectl get pods -n parcinfo -w
docker-compose ps

# Ressources utilisées
kubectl top pods -n parcinfo
docker stats
```

## 📊 Métriques et Performance

### Architecture Optimisée
- **Kubernetes** : Scalabilité et haute disponibilité
- **Docker** : Isolation et stabilité pour l'IA
- **PostgreSQL** : Performance et fiabilité
- **Cache Persistant** : Optimisation des modèles IA

### URLs de Test
- **Health Check Backend** : http://localhost:8000/health/
- **Health Check Chatbot** : http://localhost:8001/health/
- **Dashboard Garantie** : http://localhost:8501/?username=superadmin

## 🛠️ Développement

### Structure des Tests
```
tests/
├── test_github_actions.py      # Tests CI/CD
├── test_final_hybrid.py        # Tests complets
├── test_dashboard_redirect.py  # Tests redirection
└── test_final_docker_chatbot.py # Tests chatbot
```

### Workflow GitHub Actions
- Tests automatiques sur push/PR
- Validation des configurations Docker/Kubernetes
- Tests sans base de données (SQLite en mémoire)
- Vérification des imports et dépendances

## 📄 Documentation

### Fichiers de Documentation
- `ACCES-SITE.md` - Guide d'accès aux services
- `STATUT-ACCES.md` - Statut des services
- `corrections-k8s-finales.md` - Corrections Kubernetes
- `README-DOCKER.md` - Documentation Docker

## 🎉 Pour votre Soutenance

### Démonstration Live
1. **Démarrage** : `./deploy_hybrid_solution.sh`
2. **Accès** : http://localhost:8000 (Backend)
3. **Dashboard** : http://localhost:8501 (Streamlit)
4. **Chatbot** : http://localhost:8001/chatbot/
5. **Admin** : http://localhost:8000/admin/

### Points Techniques à Présenter
- ✅ **Architecture Hybride** : Kubernetes + Docker
- ✅ **IA Intégrée** : Chatbot avec Hugging Face
- ✅ **Dashboard Moderne** : Streamlit avec CSS personnalisé
- ✅ **Décharges Numériques** : PDF avec signatures
- ✅ **Tests Automatisés** : GitHub Actions
- ✅ **Déploiement** : Scripts automatisés

## 📞 Support

- **Email** : support@parcinfo.com
- **GitHub** : https://github.com/houda-aitmouch/ParcInfo
- **Issues** : GitHub Issues pour les bugs
- **Documentation** : Fichiers .md du projet

## 📄 Licence

Ce projet est sous licence MIT.

---

**🎉 ParcInfo - Solution hybride moderne pour la gestion intelligente de votre parc informatique !**

*Développé avec ❤️ en utilisant Django, React, Streamlit, Kubernetes et Docker*