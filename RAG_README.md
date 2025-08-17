# 🚀 Guide d'utilisation du système RAG de ParcInfo

## 🎯 **Qu'est-ce que le RAG ?**

Le **RAG (Retrieval-Augmented Generation)** est un système qui combine :
- **Recherche sémantique** dans la base de données
- **Génération de réponses** avec des modèles de langage (LLM)
- **Contexte intelligent** basé sur les données réelles

## ✨ **Fonctionnalités RAG activées**

### 🔍 **Recherche sémantique**
- Compréhension du sens des requêtes utilisateur
- Recherche dans tous les modèles de données (équipements, commandes, fournisseurs, etc.)
- Correspondance intelligente des concepts

### 🤖 **Réponses contextuelles**
- Réponses basées sur les données réelles de la base
- Intégration avec Ollama pour des réponses LLM avancées
- Contexte métier spécifique à ParcInfo

### 🧠 **Compréhension avancée**
- Traitement du langage naturel (NLP)
- Reconnaissance des intentions utilisateur
- Gestion des requêtes complexes

## 🚀 **Comment utiliser le RAG**

### **1. Lancement automatique avec RAG**
```bash
./launch_with_rag.sh
```

### **2. Lancement manuel avec RAG**
```bash
# Activer l'environnement virtuel RAG
source rag_env/bin/activate

# Lancer Django
python manage.py runserver
```

### **3. Test du système RAG**
```bash
python test_chatbot_rag.py
```

## 🔧 **Configuration requise**

### **Environnement virtuel RAG**
- Python 3.13+
- sentence-transformers 5.1.0+
- Django 5.2.0+
- Toutes les dépendances installées automatiquement

### **Services requis**
- ✅ Ollama (pour les réponses LLM)
- ✅ Base de données PostgreSQL
- ✅ Modèles d'embedding téléchargés automatiquement

## 📊 **Exemples d'utilisation RAG**

### **Requêtes simples**
- "Combien d'équipements informatiques avons-nous ?"
- "Quels sont nos fournisseurs ?"
- "Montrez-moi les commandes en cours"

### **Requêtes complexes**
- "Quels équipements ont plus de 2 ans de garantie ?"
- "Combien avons-nous dépensé en commandes ce mois-ci ?"
- "Quels utilisateurs ont des demandes d'équipement en attente ?"

### **Recherche sémantique**
- "Matériel de bureau" → Trouve les équipements bureautiques
- "Ordinateurs portables" → Trouve les matériels informatiques mobiles
- "Fournitures" → Trouve les commandes et équipements

## 🏗️ **Architecture RAG**

```
Utilisateur → Chatbot → RAG Manager → Base de données
                ↓
            Ollama LLM ← Embeddings ← Sentence Transformers
```

### **Composants**
1. **RAGManager** : Gestion des embeddings et recherche
2. **ParcInfoChatbot** : Interface utilisateur et logique métier
3. **SentenceTransformers** : Modèles d'embedding multilingues
4. **Ollama** : Modèles de langage locaux

## 📁 **Fichiers RAG**

- `rag_env/` : Environnement virtuel avec toutes les dépendances
- `apps/chatbot/rag_manager.py` : Gestionnaire RAG principal
- `apps/chatbot/core_chatbot.py` : Chatbot avec intégration RAG
- `launch_with_rag.sh` : Script de lancement automatique
- `test_chatbot_rag.py` : Tests du système RAG

## 🚨 **Dépannage**

### **Problème : sentence-transformers non disponible**
```bash
source rag_env/bin/activate
pip install sentence-transformers
```

### **Problème : Django ne démarre pas**
```bash
source rag_env/bin/activate
pip install -r rag_env/requirements.txt
```

### **Problème : Ollama non accessible**
```bash
# Vérifier qu'Ollama est en cours d'exécution
ollama list
```

## 🎉 **Avantages du RAG**

1. **Réponses plus précises** basées sur les données réelles
2. **Compréhension contextuelle** des requêtes utilisateur
3. **Recherche intelligente** dans toute la base de données
4. **Intégration LLM** pour des réponses naturelles
5. **Performance améliorée** grâce à la recherche sémantique

## 🔮 **Évolutions futures**

- [ ] Support multilingue avancé
- [ ] Apprentissage des préférences utilisateur
- [ ] Intégration avec d'autres modèles LLM
- [ ] Cache intelligent des embeddings
- [ ] Métriques de performance RAG

---

**💡 Le chatbot ParcInfo est maintenant équipé d'une intelligence artificielle avancée grâce au système RAG !**
