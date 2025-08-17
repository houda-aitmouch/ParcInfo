# 🚀 ParcInfo - Gestion Intelligente de Parc Informatique

## 🎯 **Description**

ParcInfo est une application web Django moderne et intelligente pour la gestion complète du parc informatique d'une entreprise. Elle intègre un **chatbot IA avancé**, des **dashboards interactifs**, et une **gestion automatisée** des équipements, demandes et livraisons.

**✨ Nouvelles fonctionnalités : Assistant IA avec RAG, Dashboard Streamlit, et interface moderne !**

## 🌟 **Fonctionnalités Principales**

### 🤖 **Assistant IA Intelligent (RAG)**
- ✅ **Chatbot IA avancé** avec recherche sémantique
- ✅ **Système RAG** (Retrieval-Augmented Generation) intégré
- ✅ **Vectorisation automatique** des modèles et documents
- ✅ **Réponses contextuelles** basées sur les données système
- ✅ **Support multilingue** et traitement naturel du langage
- ✅ **Historique des conversations** et apprentissage continu
- ✅ **Interface moderne** avec design responsive

### 📊 **Dashboards Interactifs**
- ✅ **Dashboard principal** avec métriques en temps réel
- ✅ **Dashboard de garantie** pour suivi des équipements
- ✅ **Interface Streamlit** pour analyses avancées
- ✅ **Graphiques interactifs** et visualisations
- ✅ **Filtres dynamiques** et export de données

### 🔧 **Gestion des Demandes & Équipements**
- ✅ **Demandes d'équipement** (Informatique/Bureau)
- ✅ **Système d'approbation** par gestionnaires
- ✅ **Suivi des statuts** en temps réel
- ✅ **Gestion des matériels** avec codes d'inventaire
- ✅ **Fournitures et consommables** intégrés

### 📄 **Décharges & Archives**
- ✅ **Génération automatique de PDFs**
- ✅ **Signature électronique** par canvas HTML5
- ✅ **Archivage automatique** des documents signés
- ✅ **Interface unifiée** de consultation des archives
- ✅ **Export Excel** et filtrage avancé

### 👥 **Gestion des Utilisateurs & Permissions**
- ✅ **Authentification sécurisée** avec sessions
- ✅ **Rôles personnalisés** : Employé, Gestionnaire, Super Admin
- ✅ **Système de permissions** granulaire
- ✅ **Profils utilisateurs** avec équipements assignés

### 🚚 **Logistique & Livraisons**
- ✅ **Gestion des fournisseurs** et commandes
- ✅ **Suivi des livraisons** avec validation
- ✅ **Processus de réception** automatisé
- ✅ **Rapports de livraison** et statistiques

## 🚀 **Installation Rapide**

### **Prérequis**
- Python 3.8+
- PostgreSQL ou SQLite
- pip
- Node.js (pour Tailwind CSS)

### **Installation Automatique**
```bash
# 1. Cloner le projet
git clone https://github.com/houda-aitmouch/ParcInfo.git
cd ParcInfo

# 2. Script de démarrage automatique
chmod +x startup_parcinfo.sh
./startup_parcinfo.sh

# 3. Ou installation manuelle :
python -m venv env
source env/bin/activate  # Linux/Mac
# env\Scripts\activate  # Windows

pip install -r requirements.txt
pip install -r requirements_chatbot.txt
pip install -r requirements_dashboard.txt

# 4. Configuration
cp .env.example .env
# Modifiez .env avec vos paramètres

# 5. Base de données
python manage.py makemigrations
python manage.py migrate
python manage.py setup_permissions

# 6. Super utilisateur
python manage.py createsuperuser

# 7. Lancer l'application
python manage.py runserver
```

## 🎨 **Interface & Design**

### **Technologies Frontend**
- **Tailwind CSS** pour un design moderne et responsive
- **Alpine.js** pour l'interactivité
- **Templates Django** optimisés
- **Interface mobile-first** et accessible

### **Thèmes & Personnalisation**
- **Thème sombre/clair** automatique
- **Couleurs personnalisables** par application
- **Composants réutilisables** et modulaires
- **Animations fluides** et transitions

## 🤖 **Assistant IA RAG**

### **Fonctionnalités Avancées**
- **Recherche sémantique** dans les modèles et documents
- **Vectorisation automatique** des données
- **Réponses contextuelles** basées sur l'historique
- **Apprentissage continu** des interactions
- **Support multilingue** (français, anglais, etc.)

### **Commandes de Gestion**
```bash
# Vectoriser tous les modèles
python manage.py vectorize_all_models

# Peupler l'index RAG
python manage.py populate_rag_index

# Tester la connexion Ollama
python manage.py test_ollama
```

### **Exemples d'Utilisation**
```
"Comment créer une demande d'équipement informatique ?"
"Quel est le statut de mes demandes en cours ?"
"Comment gérer le matériel de bureau ?"
"Quels sont les processus de livraison ?"
"Comment optimiser la gestion du parc ?"
```

## 📊 **Dashboards & Analytics**

### **Dashboard Principal**
- **Métriques en temps réel** des demandes
- **Statistiques des équipements** par catégorie
- **Graphiques interactifs** des tendances
- **Alertes et notifications** automatiques

### **Dashboard de Garantie**
- **Suivi des garanties** des équipements
- **Alertes d'expiration** proche
- **Historique des maintenances**
- **Coûts et budgets** de remplacement

### **Lancement des Dashboards**
```bash
# Dashboard principal
python dashboard_garantie/dashboard_garantie.py

# Dashboard simple
python dashboard_garantie/dashboard_simple.py

# Dashboard amélioré
python dashboard_garantie/launch_improved_dashboard.py
```

## 📁 **Structure du Projet**

```
ParcInfo/
├── apps/                          # Applications Django
│   ├── chatbot/                   # Assistant IA RAG
│   │   ├── core_chatbot.py       # Logique principale
│   │   ├── rag_manager.py        # Gestion RAG
│   │   ├── structured_search.py  # Recherche structurée
│   │   └── management/           # Commandes de gestion
│   ├── demande_equipement/       # Gestion des demandes
│   ├── users/                    # Gestion des utilisateurs
│   ├── fournisseurs/             # Gestion des fournisseurs
│   ├── materiel_informatique/    # Matériel informatique
│   ├── materiel_bureautique/     # Matériel de bureau
│   ├── commande_informatique/    # Commandes informatique
│   ├── commande_bureau/          # Commandes bureau
│   └── livraison/                # Gestion des livraisons
├── dashboard_garantie/           # Dashboards Streamlit
├── templates/                    # Templates HTML
├── static/                       # Fichiers statiques
│   ├── css/                      # Styles Tailwind
│   ├── js/                       # JavaScript
│   └── images/                   # Images et icônes
├── docs/                         # Documentation
├── scripts/                      # Scripts utilitaires
├── storage/                      # Stockage RAG (exclu de Git)
├── models_cache/                 # Cache des modèles IA (exclu)
└── logs/                         # Fichiers de logs (exclu)
```

## ⚙️ **Configuration Avancée**

### **Variables d'Environnement**
```bash
# .env
DEBUG=False
SECRET_KEY=votre_clé_secrète
ALLOWED_HOSTS=votre-domaine.com

# Configuration Chatbot IA
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2

# Base de données
DATABASE_URL=postgresql://user:pass@localhost/parcinfo
```

### **Configuration RAG**
```python
# settings.py
RAG_SETTINGS = {
    'vector_store_path': 'storage/',
    'embedding_model': 'paraphrase-multilingual-MiniLM-L12-v2',
    'chunk_size': 1000,
    'chunk_overlap': 200,
    'similarity_threshold': 0.7,
}
```

## 🔧 **Commandes Utiles**

### **Gestion du Chatbot IA**
```bash
# Vectoriser les modèles
python manage.py vectorize_all_models

# Peupler l'index RAG
python manage.py populate_rag_index

# Tester la connexion Ollama
python manage.py test_ollama

# Analyser les performances
python scripts/analyse_performances_chatbot.py
```

### **Maintenance & Sauvegarde**
```bash
# Sauvegarde complète
python manage.py backup_simple

# Archivage automatique
python manage.py archiver_demandes_signees

# Nettoyage des fournitures orphelines
python manage.py nettoyer_fournitures_orphelines
```

### **Développement**
```bash
# Vérification du système
python manage.py check

# Collecter les fichiers statiques
python manage.py collectstatic

# Compiler Tailwind CSS
npx tailwindcss -i ./src/input.css -o ./static/css/tailwind.css --watch
```

## 🚀 **Déploiement Production**

### **Serveur Web (Gunicorn)**
```bash
# Installation
pip install gunicorn

# Configuration
gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 120 ParcInfo.wsgi:application

# Service systemd
sudo systemctl enable parcinfo
sudo systemctl start parcinfo
```

### **Nginx Configuration**
```nginx
server {
    listen 80;
    server_name votre-domaine.com;
    
    # Fichiers statiques
    location /static/ {
        alias /chemin/vers/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Fichiers media
    location /media/ {
        alias /chemin/vers/media/;
        expires 1d;
    }
    
    # Proxy vers Django
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### **SSL avec Let's Encrypt**
```bash
# Installation Certbot
sudo apt install certbot python3-certbot-nginx

# Obtention du certificat
sudo certbot --nginx -d votre-domaine.com

# Renouvellement automatique
sudo crontab -e
# Ajouter : 0 12 * * * /usr/bin/certbot renew --quiet
```

## 📊 **Monitoring & Performance**

### **Métriques Disponibles**
- **Demandes** : total, en attente, approuvées, refusées
- **Équipements** : par catégorie, statut, garantie
- **Chatbot IA** : interactions, temps de réponse, satisfaction
- **Performance** : temps de chargement, utilisation mémoire

### **Logs & Debugging**
- **Logs d'application** : `logs/parcinfo.log`
- **Logs d'erreur** : `logs/error.log`
- **Logs du chatbot** : `logs/query_analysis_*.jsonl`
- **Monitoring temps réel** avec `monitor_dashboard.py`

## 🛠️ **Maintenance & Support**

### **Tâches Automatisées**
- **Sauvegarde quotidienne** de la base de données
- **Archivage automatique** des demandes signées
- **Nettoyage des logs** et fichiers temporaires
- **Vérification d'intégrité** des données

### **Support Technique**
- **Documentation complète** dans le dossier `docs/`
- **Guides d'installation** et de configuration
- **Scripts de diagnostic** et de réparation
- **Support communautaire** via GitHub Issues

## 📄 **Licence & Contribution**

© 2025 ParcInfo. Tous droits réservés.

**Contributions bienvenues !** 🚀
- Signaler des bugs via GitHub Issues
- Proposer des améliorations via Pull Requests
- Partager des idées et suggestions

---

**Version :** 2.0.0  
**Dernière mise à jour :** 15/08/2025  
**Développé avec ❤️ et IA 🤖**

**✨ Nouveau : Assistant IA RAG, Dashboards Streamlit, et interface moderne !**
