#!/bin/bash
# Script de lancement unifié de ParcInfo
# UN SEUL ENVIRONNEMENT : conda activate ParcInfo
# Toutes les dépendances installées dans cet environnement unique

echo "🚀 LANCEMENT UNIFIÉ DE PARCINFO"
echo "================================="
echo "✅ ENVIRONNEMENT UNIQUE : conda ParcInfo"
echo "✅ Django + RAG + Streamlit + Toutes les dépendances"
echo "✅ Plus de confusion entre plusieurs environnements"
echo ""

# Activer l'environnement conda unique
echo "🔧 Activation de l'environnement conda ParcInfo..."
source /opt/anaconda3/bin/activate ParcInfo

# Vérifier que Python est disponible
echo "🧪 Vérification de Python..."
python --version || {
    echo "❌ Python non disponible dans l'environnement conda"
    exit 1
}

# Vérifier que Django est disponible
echo "🧪 Vérification de Django..."
python -c "import django; print(f'✅ Django {django.get_version()} disponible')" || {
    echo "❌ Django non disponible dans l'environnement conda"
    exit 1
}

# Vérifier que sentence-transformers est disponible
echo "🧪 Vérification de sentence-transformers..."
python -c "import sentence_transformers; print('✅ sentence-transformers disponible')" || {
    echo "❌ sentence-transformers non disponible dans l'environnement conda"
    exit 1
}

# Vérifier que Streamlit est disponible
echo "🧪 Vérification de Streamlit..."
python -c "import streamlit; print(f'✅ Streamlit {streamlit.__version__} disponible')" || {
    echo "❌ Streamlit non disponible dans l'environnement conda"
    exit 1
}

# Test du système RAG complet
echo "🧪 Test du système RAG complet..."
python -c "
import sys
import os
import django

# Configuration Django
project_root = '/Users/HouDa/PycharmProjects/ParcInfo'
sys.path.insert(0, project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

from apps.chatbot.rag_manager import RAGManager
from apps.chatbot.core_chatbot import ParcInfoChatbot

# Test RAG Manager
rag = RAGManager()
if rag.embed_model:
    print('✅ RAG Manager: Embedding disponible')
else:
    print('❌ RAG Manager: Embedding non disponible')

# Test Chatbot
chatbot = ParcInfoChatbot()
if chatbot.nlp_available:
    print('✅ Chatbot: NLP disponible')
else:
    print('❌ Chatbot: NLP non disponible')

if chatbot.use_llm:
    print('✅ Chatbot: LLM (Ollama) disponible')
else:
    print('❌ Chatbot: LLM non disponible')

print('✅ Système RAG: Tous les composants fonctionnels')
" || {
    echo "❌ Erreur lors du test RAG"
    exit 1
}

echo ""
echo "🎉 SYSTÈME UNIFIÉ OPÉRATIONNEL !"
echo ""

# Vérifier la configuration Django
echo "🔍 Vérification de la configuration Django..."
python manage.py check || {
    echo "❌ Problèmes de configuration Django détectés"
    exit 1
}

echo ""
echo "🚀 LANCEMENT DE DJANGO AVEC RAG..."
echo "💡 Le chatbot utilisera le système RAG pour des réponses intelligentes"
echo "💡 Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

# Lancer Django
python manage.py runserver 127.0.0.1:8000
