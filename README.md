# 🏢 ParcInfo - Gestion de Parc Informatique

## 📋 Vue d'Ensemble

**ParcInfo** est une application web complète de gestion de parc informatique développée avec Django et React. Elle permet la gestion des équipements informatiques et de bureau, des demandes d'équipement, des commandes, des fournisseurs et des livraisons.

## ✨ Fonctionnalités Principales

### 🔧 Gestion des Équipements
- **Matériel Informatique** : Ordinateurs, serveurs, périphériques
- **Matériel de Bureau** : Mobilier, accessoires
- **Fournitures** : Consommables, accessoires
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
│   ├── ui/                    # Composants UI réutilisables
│   ├── Dashboard.tsx          # Tableau de bord
│   ├── Demandes.tsx           # Gestion des demandes
│   ├── CommandesIT.tsx        # Commandes informatiques
│   ├── CommandesBureau.tsx    # Commandes bureau
│   ├── MaterielsIT.tsx        # Matériel informatique
│   ├── MaterielsBureau.tsx    # Matériel de bureau
│   ├── Fournisseurs.tsx       # Gestion fournisseurs
│   ├── Livraisons.tsx         # Suivi livraisons
│   └── Chatbot.tsx            # Assistant IA
├── contexts/                  # Contextes React
├── styles/                    # Styles CSS
└── assets/                    # Ressources
```

## 🚀 Installation et Configuration

### Prérequis
- Python 3.8+
- Node.js 16+
- PostgreSQL (recommandé) ou SQLite
- Git

### Installation Backend

1. **Cloner le projet**
```bash
git clone https://github.com/votre-repo/parcinfo.git
cd parcinfo
```

2. **Créer l'environnement virtuel**
```bash
python -m venv rag_env
source rag_env/bin/activate  # Linux/Mac
# ou
rag_env\Scripts\activate     # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configuration de la base de données**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Créer un super utilisateur**
```bash
python manage.py createsuperuser
```

6. **Lancer le serveur de développement**
```bash
python manage.py runserver
```

### Installation Frontend

1. **Installer les dépendances**
```bash
cd frontend
npm install
```

2. **Lancer le serveur de développement**
```bash
npm run dev
```

## 🔧 Configuration

### Variables d'Environnement

Créer un fichier `.env` à la racine du projet :

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

### Configuration du Chatbot

1. **Installer les dépendances RAG**
```bash
pip install -r requirements_chatbot.txt
```

2. **Configurer l'index vectoriel**
```bash
python manage.py populate_rag_index
```

## 📊 Structure des Données

### Modèles Principaux

#### Utilisateurs
- **CustomUser** : Utilisateurs avec rôles et permissions
- **NotificationDemande** : Notifications pour les demandes

#### Équipements
- **MaterielInformatique** : Matériel informatique
- **MaterielBureau** : Matériel de bureau
- **Fourniture** : Fournitures et consommables

#### Demandes et Commandes
- **DemandeEquipement** : Demandes d'équipement
- **CommandeInformatique** : Commandes informatiques
- **CommandeBureau** : Commandes bureau
- **LigneCommande** : Lignes de commande

#### Fournisseurs et Livraisons
- **Fournisseur** : Fournisseurs
- **Livraison** : Livraisons
- **LigneLivraison** : Lignes de livraison

## 🔐 Système de Permissions

### Rôles Utilisateurs

1. **Employé**
   - Créer des demandes d'équipement
   - Consulter ses équipements affectés
   - Signer des décharges
   - Recevoir des notifications

2. **Gestionnaire Informatique**
   - Gérer les demandes informatiques
   - Approuver/rejeter les demandes
   - Gérer le matériel informatique
   - Suivre les commandes informatiques

3. **Gestionnaire Bureau**
   - Gérer les demandes bureau
   - Approuver/rejeter les demandes
   - Gérer le matériel de bureau
   - Suivre les commandes bureau

4. **Super Admin**
   - Accès complet à toutes les fonctionnalités
   - Gestion des utilisateurs
   - Configuration système

## 🔔 Système de Notifications

### Fonctionnalités
- **Notifications Automatiques** : Créées lors des changements de statut
- **Messages Contextuels** : Détails spécifiques selon le type de demande
- **Interface Optimisée** : Affichage propre sans duplication
- **Filtrage par Rôle** : Seuls les employés reçoivent des notifications

### Exemples de Messages
- **Approbation** : "🎉 Votre demande de matériel informatique (Ordinateur portable) a été approuvée ! Veuillez signer la décharge pour recevoir l'équipement."
- **Rejet** : "❌ Votre demande de matériel informatique a été rejetée. Contactez votre responsable pour plus de détails."

## 🤖 Chatbot IA

### Fonctionnalités
- **Assistant Intelligent** : Réponses automatiques aux questions
- **Base de Connaissances** : Documentation intégrée
- **Recherche Sémantique** : RAG pour des réponses précises
- **Interface Chat** : Interface utilisateur intuitive

### Configuration
```bash
# Installer les dépendances IA
pip install -r requirements_chatbot.txt

# Configurer l'index vectoriel
python manage.py populate_rag_index

# Lancer le chatbot
python manage.py runserver
```

## 📱 Interface Utilisateur

### Technologies Frontend
- **React 18** : Interface utilisateur moderne
- **TypeScript** : Typage statique
- **Tailwind CSS** : Styles utilitaires
- **Alpine.js** : Interactivité légère
- **Vite** : Build tool rapide

### Composants Principaux
- **Dashboard** : Vue d'ensemble personnalisée
- **Demandes** : Gestion des demandes d'équipement
- **Commandes** : Suivi des commandes
- **Matériels** : Gestion des équipements
- **Fournisseurs** : Catalogue des fournisseurs
- **Chatbot** : Assistant IA intégré

## 🧪 Tests

### Tests Backend
```bash
# Tests unitaires
python manage.py test

# Tests spécifiques
python manage.py test apps.demande_equipement
python manage.py test apps.users
```

### Tests Frontend
```bash
cd frontend
npm test
```

## 📈 Déploiement

### Production avec Docker

1. **Créer Dockerfile**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "ParcInfo.wsgi:application"]
```

2. **Docker Compose**
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db/parcinfo
    depends_on:
      - db
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=parcinfo
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
```

### Déploiement Cloud

#### Heroku
```bash
# Installer Heroku CLI
heroku create parcinfo-app
heroku config:set SECRET_KEY=votre-secret-key
git push heroku main
```

#### AWS
- **EC2** : Serveur d'application
- **RDS** : Base de données PostgreSQL
- **S3** : Stockage des fichiers
- **CloudFront** : CDN pour les assets

## 🔧 Maintenance

### Sauvegarde
```bash
# Sauvegarde de la base de données
python manage.py dumpdata > backup.json

# Restauration
python manage.py loaddata backup.json
```

### Mise à Jour
```bash
# Mettre à jour les dépendances
pip install -r requirements.txt --upgrade

# Appliquer les migrations
python manage.py migrate

# Redémarrer les services
sudo systemctl restart parcinfo
```

### Monitoring
- **Logs** : Django logging configuré
- **Métriques** : Performance monitoring
- **Alertes** : Notifications d'erreurs

## 📚 Documentation

### Guides Utilisateur
- [Guide d'Utilisation](docs/GUIDE_UTILISATEUR.md)
- [Guide Administrateur](docs/GUIDE_ADMINISTRATEUR.md)
- [Guide Technique](docs/GUIDE_TECHNIQUE.md)

### API Documentation
- [API REST](docs/API.md)
- [Endpoints](docs/ENDPOINTS.md)
- [Authentification](docs/AUTH.md)

### Développement
- [Architecture](docs/ARCHITECTURE.md)
- [Contributing](docs/CONTRIBUTING.md)
- [Changelog](docs/CHANGELOG.md)


### Standards de Code
- **Python** : PEP 8, Black, Flake8
- **JavaScript** : ESLint, Prettier
- **Tests** : Coverage > 80%
- **Documentation** : Docstrings, README


**ParcInfo** - Gestion intelligente de votre parc informatique 🚀
