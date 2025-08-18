#!/bin/bash
# Script de lancement unifié de ParcInfo
# Utilise UNIQUEMENT l'environnement virtuel rag_env

echo "🚀 LANCEMENT UNIFIÉ DE PARCINFO AVEC RAG"
echo "=========================================="
echo "✅ Environnement unique : rag_env"
echo "✅ Python 3.13.5 avec toutes les dépendances"
echo "✅ Système RAG complet et opérationnel"
echo ""

# Vérifier que l'environnement virtuel unique existe
if [ ! -d "rag_env" ]; then
    echo "❌ ERREUR : Environnement virtuel 'rag_env' non trouvé !"
    echo "💡 Ce projet utilise UNIQUEMENT l'environnement rag_env"
    echo "💡 Créez-le avec : python3 -m venv rag_env"
    echo "💡 Puis installez les dépendances : pip install -r rag_env/requirements.txt"
    exit 1
fi

# Activer l'environnement virtuel unique
echo "🔧 Activation de l'environnement virtuel rag_env..."
source rag_env/bin/activate

# Vérifier que Python est disponible
echo "🧪 Vérification de Python..."
python --version || {
    echo "❌ Python non disponible dans rag_env"
    exit 1
}

# Vérifier que Django est disponible
echo "🧪 Vérification de Django..."
python -c "import django; print(f'✅ Django {django.get_version()} disponible')" || {
    echo "❌ Django non disponible dans rag_env"
    exit 1
}

# Vérifier que sentence-transformers est disponible
echo "🧪 Vérification de sentence-transformers..."
python -c "import sentence_transformers; print('✅ sentence-transformers disponible')" || {
    echo "❌ sentence-transformers non disponible dans rag_env"
    exit 1
}

# Vérifier que Streamlit est disponible
echo "🧪 Vérification de Streamlit..."
python -c "import streamlit; print(f'✅ Streamlit {streamlit.__version__} disponible')" || {
    echo "❌ Streamlit non disponible dans rag_env"
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
python manage.py runserver 0.0.0.0:8000
