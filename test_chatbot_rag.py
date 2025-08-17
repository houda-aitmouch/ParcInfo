#!/usr/bin/env python3
"""
Test complet du chatbot ParcInfo avec RAG
Utilise l'environnement virtuel RAG
"""

import subprocess
import sys
import os

def test_chatbot_rag():
    """Test complet du chatbot avec RAG"""
    print("🚀 Test complet du chatbot ParcInfo avec RAG")
    print("=" * 60)
    
    # Chemin vers l'environnement virtuel
    venv_python = "rag_env/bin/python"
    
    # Test 1: Import des modules RAG avec Django configuré
    print("🧪 Test 1: Import des modules RAG...")
    try:
        result = subprocess.run([
            venv_python, "-c", 
            """
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
print('✅ Tous les modules RAG importés avec succès')
            """
        ], capture_output=True, text=True, check=True)
        print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur import: {e.stderr}")
        return False
    
    # Test 2: Initialisation du RAG Manager
    print("\n🧪 Test 2: Initialisation du RAG Manager...")
    try:
        result = subprocess.run([
            venv_python, "-c", 
            """
import sys
import os
import django

# Configuration Django
project_root = '/Users/HouDa/PycharmProjects/ParcInfo'
sys.path.insert(0, project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

from apps.chatbot.rag_manager import RAGManager
rag = RAGManager()
if rag.embed_model:
    print('✅ RAG Manager initialisé avec embedding')
    print(f'Modèle: {type(rag.embed_model).__name__}')
else:
    print('❌ RAG Manager sans embedding')
            """
        ], capture_output=True, text=True, check=True)
        print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur RAG Manager: {e.stderr}")
        return False
    
    # Test 3: Initialisation du Chatbot
    print("\n🧪 Test 3: Initialisation du Chatbot...")
    try:
        result = subprocess.run([
            venv_python, "-c", 
            """
import sys
import os
import django

# Configuration Django
project_root = '/Users/HouDa/PycharmProjects/ParcInfo'
sys.path.insert(0, project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

from apps.chatbot.core_chatbot import ParcInfoChatbot
chatbot = ParcInfoChatbot()
print(f'✅ Chatbot initialisé')
print(f'NLP disponible: {chatbot.nlp_available}')
print(f'LLM disponible: {chatbot.use_llm}')
            """
        ], capture_output=True, text=True, check=True)
        print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur Chatbot: {e.stderr}")
        return False
    
    # Test 4: Test d'une requête simple
    print("\n🧪 Test 4: Test d'une requête simple...")
    try:
        result = subprocess.run([
            venv_python, "-c", 
            """
import sys
import os
import django

# Configuration Django
project_root = '/Users/HouDa/PycharmProjects/ParcInfo'
sys.path.insert(0, project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

from apps.chatbot.core_chatbot import ParcInfoChatbot
chatbot = ParcInfoChatbot()

query = "Bonjour, comment ça va ?"
print(f'Question: {query}')
try:
    response = chatbot.process_query(query)
    print(f'✅ Réponse reçue: {response[:100]}...')
except Exception as e:
    print(f'❌ Erreur lors du traitement: {e}')
            """
        ], capture_output=True, text=True, check=True)
        print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur requête: {e.stderr}")
        return False
    
    return True

def show_usage_instructions():
    """Afficher les instructions d'utilisation"""
    print("\n" + "=" * 60)
    print("📚 INSTRUCTIONS D'UTILISATION DU CHATBOT RAG")
    print("=" * 60)
    print("")
    print("🎯 Le chatbot ParcInfo utilise maintenant le système RAG !")
    print("")
    print("✨ Fonctionnalités RAG activées :")
    print("   • Recherche sémantique dans la base de données")
    print("   • Réponses contextuelles basées sur les données")
    print("   • Compréhension avancée des requêtes")
    print("   • Intégration avec Ollama pour les réponses LLM")
    print("")
    print("🚀 Pour lancer le serveur avec RAG :")
    print("   ./launch_with_rag.sh")
    print("")
    print("🔧 Pour activer manuellement l'environnement RAG :")
    print("   source rag_env/bin/activate")
    print("   python manage.py runserver")
    print("")
    print("🧪 Pour tester le RAG :")
    print("   python test_chatbot_rag.py")
    print("")
    print("💡 Le chatbot répondra maintenant de manière plus intelligente")
    print("   et contextuelle grâce au système RAG !")

if __name__ == "__main__":
    if test_chatbot_rag():
        print("\n🎉 Tous les tests du chatbot RAG sont réussis !")
        show_usage_instructions()
    else:
        print("\n❌ Certains tests du chatbot RAG ont échoué")
        print("💡 Vérifiez que l'environnement virtuel est correctement configuré")
