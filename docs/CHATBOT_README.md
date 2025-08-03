# Assistant ParcInfo - Chatbot avec LLaMA 3 et LangChain

## Vue d'ensemble

L'Assistant ParcInfo est un chatbot intelligent intégré au système de gestion de parc informatique et bureautique. Il utilise LLaMA 3 et LangChain pour fournir des réponses contextuelles et personnalisées aux utilisateurs.

## Fonctionnalités

### 🎯 Fonctionnalités principales
- **Chat en temps réel** : Interface de chat moderne et responsive
- **Réponses contextuelles** : Le chatbot accède aux données de l'utilisateur pour des réponses personnalisées
- **Historique des conversations** : Sauvegarde et consultation des conversations passées
- **Restrictions d'accès** : Disponible uniquement pour les employés (pas pour les superadmins et gestionnaires)
- **Interface moderne** : Design épuré avec animations et indicateurs de frappe

### 🤖 Intelligence Artificielle
- **LLaMA 3** : Modèle de langage avancé pour la compréhension et la génération de réponses
- **LangChain** : Framework pour la gestion des chaînes de conversation
- **Vectorstore** : Stockage vectoriel pour la recherche sémantique
- **Embeddings** : Représentations vectorielles pour la compréhension du contexte

### 📊 Intégration avec la base de données
- **Contexte utilisateur** : Accès aux demandes d'équipement de l'utilisateur
- **Matériel assigné** : Consultation du matériel informatique et bureautique
- **Statuts en temps réel** : Informations sur les livraisons et demandes
- **Données système** : Statistiques globales du système ParcInfo

## Architecture

### Structure des fichiers
```
apps/chatbot/
├── __init__.py
├── admin.py          # Interface d'administration
├── apps.py           # Configuration de l'application
├── forms.py          # Formulaires
├── llm_engine.py     # Moteur LLM avec LLaMA 3 et LangChain
├── models.py         # Modèle ChatMessage
├── tests.py          # Tests unitaires
├── urls.py           # Configuration des URLs
├── views.py          # Vues Django
└── migrations/       # Migrations de base de données
```

### Composants principaux

#### 1. ParcInfoChatbot (llm_engine.py)
- **Initialisation LLM** : Configuration de LLaMA 3 ou fallback vers HuggingFace
- **Vectorstore** : Stockage et recherche de documents contextuels
- **Chaîne de conversation** : Gestion du dialogue avec mémoire
- **Contexte base de données** : Récupération des données système

#### 2. Interface de chat (views.py)
- **Chat interface** : Interface principale de conversation
- **Chat API** : Endpoint REST pour les requêtes de chat
- **Historique** : Gestion des conversations passées
- **Aide** : Documentation et guide d'utilisation

#### 3. Modèle de données (models.py)
- **ChatMessage** : Stockage des conversations utilisateur
- **Session tracking** : Suivi des sessions de conversation
- **Timestamps** : Horodatage des interactions

## Installation et configuration

### 1. Dépendances requises
```bash
pip install langchain langchain-community langchain-core
pip install llama-cpp-python sentence-transformers
pip install chromadb faiss-cpu numpy pandas
pip install transformers torch accelerate
```

### 2. Configuration Django
Ajouter l'application aux `INSTALLED_APPS` :
```python
INSTALLED_APPS = [
    # ... autres applications
    'apps.chatbot.apps.ChatbotConfig',
]
```

### 3. URLs
Ajouter les URLs du chatbot :
```python
urlpatterns = [
    # ... autres URLs
    path('chatbot/', include('apps.chatbot.urls', namespace='chatbot')),
]
```

### 4. Migrations
```bash
python manage.py makemigrations chatbot
python manage.py migrate
```

## Utilisation

### Accès au chatbot
- **URL** : `/chatbot/`
- **Permissions** : Employés uniquement (pas de superadmin/gestionnaire)
- **Authentification** : Requise

### Interface utilisateur
1. **Page d'accueil** : Interface de chat principale
2. **Historique** : Consultation des conversations passées
3. **Aide** : Guide d'utilisation et exemples
4. **Effacement** : Suppression de l'historique personnel

### Exemples de questions
- "Comment faire une demande d'équipement ?"
- "Quel est le statut de mes demandes ?"
- "Où puis-je voir mon matériel informatique ?"
- "Comment suivre une livraison ?"
- "Quels sont les types d'équipements disponibles ?"

## Configuration avancée

### Modèle LLaMA 3
Pour utiliser un modèle LLaMA 3 local :
```bash
# Télécharger un modèle GGUF
wget https://huggingface.co/TheBloke/Llama-3-8B-Instruct-GGUF/resolve/main/llama-3-8b-instruct.Q4_K_M.gguf

# Définir le chemin dans les variables d'environnement
export LLAMA_MODEL_PATH="./models/llama-3-8b-instruct.Q4_K_M.gguf"
```

### Vectorstore
Le vectorstore utilise ChromaDB par défaut :
- **Persistance** : `./chroma_db/`
- **Embeddings** : `sentence-transformers/all-MiniLM-L6-v2`
- **Documents** : Contexte système + données utilisateur

### Personnalisation des réponses
Modifier `llm_engine.py` pour :
- Ajuster les prompts
- Ajouter de nouveaux types de réponses
- Intégrer d'autres sources de données

## Sécurité et permissions

### Restrictions d'accès
- **Superadmins** : Accès refusé
- **Gestionnaires** : Accès refusé
- **Employés** : Accès complet

### Protection des données
- **Isolation** : Chaque utilisateur ne voit que ses propres conversations
- **Session tracking** : Identification unique des sessions
- **CSRF protection** : Protection contre les attaques CSRF

## Tests

### Exécution des tests
```bash
python manage.py test apps.chatbot
```

### Tests disponibles
- **Accès** : Vérification des restrictions d'accès
- **API** : Tests des endpoints de chat
- **Modèle** : Validation du modèle ChatMessage
- **Fonctionnalités** : Tests des fonctionnalités principales

## Maintenance

### Surveillance
- **Logs** : Surveiller les erreurs d'initialisation LLM
- **Performance** : Temps de réponse des requêtes
- **Utilisation** : Statistiques d'utilisation du chatbot

### Sauvegarde
- **Base de données** : Sauvegarde régulière de la table `chat_message`
- **Vectorstore** : Sauvegarde du dossier `chroma_db/`
- **Modèles** : Sauvegarde des modèles LLM

## Dépannage

### Problèmes courants

#### 1. Erreur d'initialisation LLM
```
Erreur lors de l'initialisation du LLM
```
**Solution** : Vérifier que les modèles sont téléchargés et accessibles

#### 2. Erreur de vectorstore
```
Erreur lors de l'initialisation du vectorstore
```
**Solution** : Vérifier les permissions sur le dossier `chroma_db/`

#### 3. Réponses vides
**Solution** : Le chatbot utilise le mode fallback avec des réponses prédéfinies

### Logs et debugging
- Activer le mode verbose dans `llm_engine.py`
- Consulter les logs Django
- Vérifier les erreurs dans la console JavaScript

## Évolutions futures

### Améliorations prévues
- **Multilingue** : Support de plusieurs langues
- **Voice** : Interface vocale
- **Analytics** : Statistiques d'utilisation avancées
- **Intégration** : Connexion avec d'autres systèmes

### Extensions possibles
- **Plugins** : Système de plugins pour étendre les fonctionnalités
- **API externe** : Interface pour intégrations tierces
- **Machine Learning** : Amélioration continue des réponses

## Support

Pour toute question ou problème :
1. Consulter la documentation
2. Vérifier les logs d'erreur
3. Contacter l'équipe de développement

---

**Note** : Ce chatbot est conçu pour être un assistant intelligent et utile pour les utilisateurs du système ParcInfo, en respectant les bonnes pratiques de sécurité et de performance. 