#!/bin/bash
"""
Script de lancement de ParcInfo avec RAG activé
Utilise l'environnement virtuel avec sentence-transformers
"""

echo "🚀 Lancement de ParcInfo avec RAG activé"
echo "=========================================="

# Vérifier que l'environnement virtuel existe
if [ ! -d "rag_env" ]; then
    echo "❌ Environnement virtuel 'rag_env' non trouvé"
    echo "💡 Créez-le avec: python3 -m venv rag_env"
    echo "💡 Puis installez les dépendances: source rag_env/bin/activate && pip install sentence-transformers django python-dotenv"
    exit 1
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source rag_env/bin/activate

# Vérifier que sentence-transformers est disponible
echo "🧪 Vérification de sentence-transformers..."
python -c "import sentence_transformers; print('✅ sentence-transformers disponible')" || {
    echo "❌ sentence-transformers non disponible dans l'environnement virtuel"
    echo "💡 Installez-le avec: pip install sentence-transformers"
    exit 1
}

# Vérifier que Django est disponible
echo "🧪 Vérification de Django..."
python -c "import django; print(f'✅ Django {django.get_version()} disponible')" || {
    echo "❌ Django non disponible dans l'environnement virtuel"
    echo "💡 Installez-le avec: pip install django"
    exit 1
}

# Test du système RAG
echo "🧪 Test du système RAG..."
python -c "
from apps.chatbot.rag_manager import RAGManager
from apps.chatbot.core_chatbot import ParcInfoChatbot

# Test RAG Manager
rag = RAGManager()
if rag.embed_model:
    print('✅ RAG Manager initialisé avec embedding')
else:
    print('❌ RAG Manager sans embedding')

# Test Chatbot
chatbot = ParcInfoChatbot()
if chatbot.nlp_available:
    print('✅ Chatbot avec NLP disponible')
else:
    print('❌ Chatbot sans NLP')
" || {
    echo "❌ Erreur lors du test RAG"
    echo "💡 Vérifiez que Django est configuré correctement"
    exit 1
}

echo ""
echo "🎉 Système RAG opérationnel !"
echo ""

# Lancer Django
echo "🚀 Lancement de Django avec RAG..."
echo "💡 Le chatbot utilisera maintenant le système RAG pour des réponses plus précises"
echo "💡 Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

python manage.py runserver 0.0.0.0:8000
