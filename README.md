# 📚 ParcInfo - Gestion de Parc Informatique

## 🎯 **Description**

ParcInfo est une application web Django pour la gestion complète du parc informatique d'une entreprise. Elle permet de gérer les demandes d'équipement, les décharges électroniques, et l'archivage automatique des documents. **Nouveau : Assistant IA intégré avec LLaMA 3 !**

## ✨ **Fonctionnalités Principales**

### 🔧 **Gestion des Demandes**
- ✅ Création de demandes d'équipement (Informatique/Bureau)
- ✅ Approbation par les gestionnaires
- ✅ Suivi des statuts (En attente, Approuvée, Refusée)
- ✅ Gestion des matériels et fournitures

### 📄 **Décharges Électroniques**
- ✅ Génération automatique de PDFs
- ✅ Signature électronique par canvas HTML5
- ✅ Archivage automatique des décharges signées
- ✅ Interface unifiée de consultation des archives

### 🤖 **Assistant IA LLaMA 3**
- ✅ Chatbot intelligent avec LLaMA 3
- ✅ Réponses contextuelles basées sur les données système
- ✅ Support NLP avancé pour questions naturelles
- ✅ Mode fallback si LLaMA 3 indisponible
- ✅ Adaptation au rôle utilisateur
- ✅ Historique des conversations
- ✅ Insights d'apprentissage

### 👥 **Gestion des Utilisateurs**
- ✅ Authentification sécurisée
- ✅ Rôles : Employé, Gestionnaire Informatique, Gestionnaire Bureau, Super Admin
- ✅ Permissions automatiques selon les catégories

### 📊 **Archives et Rapports**
- ✅ Archivage électronique automatique
- ✅ Export Excel des archives
- ✅ Filtrage par catégorie, type, dates
- ✅ Statistiques en temps réel

## 🚀 **Installation**

### **Prérequis**
- Python 3.8+
- PostgreSQL
- pip
- (Optionnel) Modèle LLaMA 3 pour le chatbot IA

### **Installation Rapide**
```bash
# 1. Cloner le projet
git clone <repository-url>
cd ParcInfo

# 2. Configuration automatique
python scripts/setup_project.py

# 3. Créer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Configurer les variables d'environnement
# Modifiez le fichier .env avec vos paramètres

# 6. Migrations
python manage.py makemigrations
python manage.py migrate

# 7. Créer un super utilisateur
python manage.py createsuperuser

# 8. (Optionnel) Télécharger LLaMA 3 pour le chatbot
# Placez le modèle dans models/llama-3-8b-instruct.gguf

# 9. Lancer le serveur
python manage.py runserver
```

## ⚙️ **Configuration**

### **Base de Données**
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'parcinfo_db',
        'USER': 'votre_utilisateur',
        'PASSWORD': 'votre_mot_de_passe',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### **Variables d'Environnement**
```bash
# .env
DEBUG=False
SECRET_KEY=votre_clé_secrète
ALLOWED_HOSTS=votre-domaine.com

# Configuration Chatbot LLaMA 3
LLAMA_MODEL_PATH=models/llama-3-8b-instruct.gguf
```

### **Configuration LLaMA 3 (Optionnel)**
```bash
# 1. Télécharger le modèle depuis HuggingFace
# https://huggingface.co/TheBloke/Llama-3-8B-Instruct-GGUF

# 2. Créer le dossier models/
mkdir models

# 3. Placer le fichier .gguf dans models/
# Exemple: models/llama-3-8b-instruct.gguf

# 4. Le chatbot utilisera automatiquement LLaMA 3
# Sinon, il fonctionnera en mode fallback
```

## 📁 **Structure du Projet**

```
ParcInfo/
├── apps/
│   ├── demande_equipement/     # Gestion des demandes
│   ├── users/                  # Gestion des utilisateurs
│   ├── fournisseurs/           # Gestion des fournisseurs
│   ├── materiel_informatique/  # Matériel informatique
│   ├── materiel_bureautique/   # Matériel de bureau
│   ├── commande_informatique/  # Commandes informatique
│   ├── commande_bureau/        # Commandes bureau
│   ├── livraison/              # Gestion des livraisons
│   └── chatbot/                # Assistant IA LLaMA 3
├── models/                     # Modèles LLaMA 3 (optionnel)
├── templates/                  # Templates HTML
├── static/                     # Fichiers statiques
├── media/                      # Fichiers uploadés
├── docs/                       # Documentation
└── scripts/                    # Scripts utilitaires
```

## 🤖 **Assistant IA LLaMA 3**

### **Fonctionnalités**
- **Réponses intelligentes** : Utilise LLaMA 3 pour comprendre et répondre aux questions
- **Contexte système** : Accède aux données en temps réel (demandes, matériel, etc.)
- **Adaptation rôle** : Réponses personnalisées selon le rôle utilisateur
- **Mode fallback** : Fonctionne même sans LLaMA 3
- **Interface moderne** : Chat en temps réel avec historique

### **Exemples de Questions**
```
"Comment faire une demande d'équipement ?"
"Quel est le statut de mes demandes ?"
"Comment gérer le matériel informatique ?"
"Quels sont les processus de livraison ?"
"Comment optimiser la gestion du parc ?"
"Quelles sont les règles d'approbation ?"
```

### **Accès**
- **URL** : `/chatbot/`
- **Permissions** : Tous les utilisateurs connectés
- **Historique** : `/chatbot/history/`
- **Aide** : `/chatbot/help/`

## 🔧 **Commandes Utiles**

### **Sauvegarde**
```bash
# Sauvegarde complète
python manage.py backup_simple

# Sauvegarde base de données seulement
python manage.py backup_simple --db-only

# Sauvegarde fichiers seulement
python manage.py backup_simple --files-only
```

### **Archivage**
```bash
# Archiver toutes les demandes signées
python manage.py archiver_demandes_signees

# Mode test (dry-run)
python manage.py archiver_demandes_signees --dry-run
```

### **Maintenance**
```bash
# Vérification du système
python manage.py check

# Collecter les fichiers statiques
python manage.py collectstatic

# Nettoyer les anciens fichiers
python manage.py cleanup_old_files
```

## 🔐 **Sécurité**

### **Authentification**
- Sessions sécurisées (1 heure d'expiration)
- Mots de passe forts (minimum 10 caractères)
- Protection CSRF activée

### **Permissions**
- Gestionnaire Informatique : Accès aux archives informatiques
- Gestionnaire Bureau : Accès aux archives bureau
- Super Admin : Accès complet à toutes les fonctionnalités

### **Sauvegarde**
- Sauvegarde automatique de la base de données
- Archivage des fichiers media
- Rétention des sauvegardes (30 jours)

## 📊 **Monitoring**

### **Métriques Disponibles**
- Nombre total de demandes
- Demandes en attente
- Décharges signées
- Archives créées
- Temps de réponse moyen
- Interactions chatbot IA

### **Logs**
- Logs d'application dans `logs/parcinfo.log`
- Logs d'erreur automatiques
- Monitoring des performances

## 🚀 **Déploiement Production**

### **Serveur Web**
```bash
# Installation Gunicorn
pip install gunicorn

# Configuration
gunicorn --bind 0.0.0.0:8000 ParcInfo.wsgi:application
```

### **Nginx**
```nginx
server {
    listen 80;
    server_name votre-domaine.com;
    
    location /static/ {
        alias /chemin/vers/static/;
    }
    
    location /media/ {
        alias /chemin/vers/media/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### **SSL (Let's Encrypt)**
```bash
# Installation Certbot
sudo apt install certbot python3-certbot-nginx

# Obtention du certificat
sudo certbot --nginx -d votre-domaine.com
```

## 🛠️ **Maintenance**

### **Tâches Quotidiennes**
- Sauvegarde automatique
- Nettoyage des logs
- Vérification de l'intégrité

### **Tâches Hebdomadaires**
- Archivage des anciennes données
- Optimisation de la base de données
- Mise à jour des statistiques

### **Tâches Mensuelles**
- Révision des permissions
- Audit de sécurité
- Sauvegarde complète

## 📞 **Support**

### **Contact Technique**
- Email : support@votre-entreprise.com
- Téléphone : +33 1 23 45 67 89

### **Documentation**
- Guide utilisateur : `/docs/GUIDE_UTILISATEUR.md`
- Guide administrateur : `/docs/GUIDE_ADMINISTRATEUR.md`
- API documentation : `/docs/API.md`

## 📄 **Licence**

© 2025 Votre Entreprise. Tous droits réservés.

---

**Version :** 1.1.0  
**Dernière mise à jour :** 31/07/2025  
**Développé avec ❤️ pour votre entreprise**

**Nouveau : Assistant IA LLaMA 3 intégré ! 🤖**
