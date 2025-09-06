# ParcInfo - Gestion de Parc Informatique

## Vue d'Ensemble

**ParcInfo** est une application web complète de gestion de parc informatique développée avec Django, React et Streamlit. Elle utilise une architecture hybride Kubernetes + Docker pour une performance optimale et une scalabilité maximale.

##  Fonctionnalités Principales

### Gestion des Équipements
- **Matériel Informatique** : Ordinateurs, serveurs, périphériques
- **Matériel de Bureau** : Mobilier, accessoires
- **Suivi d'Inventaire** : Codes d'inventaire, statuts, affectations
- **Décharges Numériques** : Signatures électroniques avec PDF

###  Gestion des Demandes
- **Demandes d'Équipement** : Création, suivi, approbation
- **Workflow d'Approbation** : Hiérarchie des validations
- **Signatures Électroniques** : Décharges numériques
- **Notifications Automatiques** : Système de notifications en temps réel

### Gestion des Commandes
- **Commandes Informatiques** : Matériel informatique
- **Commandes Bureau** : Matériel de bureau
- **Gestion des Fournisseurs** : Catalogue, contacts, devis
- **Suivi des Livraisons** : Statuts, dates, réceptions

### Gestion des Utilisateurs
- **Rôles et Permissions** : Employé, Gestionnaire, Super Admin
- **Profils Personnalisés** : Informations, équipements affectés
- **Authentification Sécurisée** : Login/logout, sessions

### Chatbot Intelligent
- **Assistant IA** : Réponses automatiques aux questions
- **Base de Connaissances** : Documentation intégrée
- **Recherche Sémantique** : RAG (Retrieval-Augmented Generation)
- **Modèles Hugging Face** : sentence-transformers pour l'IA

### Dashboard de Garanties
- **Interface Streamlit** : Dashboard interactif et moderne
- **Visualisations** : Graphiques et métriques en temps réel
- **Gestion des Garanties** : Suivi et alertes automatiques

##  Architecture Technique

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

##  Installation et Configuration

### Prérequis
- Python 3.8+
- Node.js 16+
- PostgreSQL
- Docker & Docker Compose
- Kubernetes (Docker Desktop ou Minikube)
- kubectl


##  Fonctionnalités Avancées

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

##  Déploiement en Production

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

##  Métriques et Performance

### Architecture Optimisée
- **Kubernetes** : Scalabilité et haute disponibilité
- **Docker** : Isolation et stabilité pour l'IA
- **PostgreSQL** : Performance et fiabilité
- **Cache Persistant** : Optimisation des modèles IA

### URLs de Test
- **Health Check Backend** : http://localhost:8000/health/
- **Health Check Chatbot** : http://localhost:8001/health/
- **Dashboard Garantie** : http://localhost:8501/?username=superadmin


### Workflow GitHub Actions
- Tests automatiques sur push/PR
- Validation des configurations Docker/Kubernetes
- Tests sans base de données (SQLite en mémoire)
- Vérification des imports et dépendances

