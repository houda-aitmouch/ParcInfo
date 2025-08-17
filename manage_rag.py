#!/usr/bin/env /usr/bin/python3
"""
Script de gestion RAG pour ParcInfo
Utilise le Python système avec sentence-transformers installé
"""

import os
import sys
import django
from pathlib import Path

# Ajouter le répertoire du projet au PYTHONPATH
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

def test_rag():
    """Test du système RAG"""
    print("🧪 Test du système RAG...")
    
    try:
        from apps.chatbot.rag_manager import RAGManager
        from apps.chatbot.core_chatbot import ParcInfoChatbot
        
        print("✅ Import des modules RAG réussi")
        
        # Test du RAG Manager
        rag = RAGManager()
        if rag.embed_model:
            print("✅ Modèle d'embedding initialisé")
        else:
            print("❌ Modèle d'embedding non disponible")
            
        # Test du chatbot
        chatbot = ParcInfoChatbot()
        if chatbot.nlp_available:
            print("✅ Chatbot avec NLP disponible")
        else:
            print("❌ Chatbot sans NLP")
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test RAG: {e}")
        return False

def populate_rag_index():
    """Peupler l'index RAG"""
    print("🔄 Peuplement de l'index RAG...")
    
    try:
        from apps.chatbot.rag_manager import RAGManager
        
        rag = RAGManager()
        if not rag.embed_model:
            print("❌ Modèle d'embedding non disponible")
            return False
            
        count = rag.populate_index()
        print(f"✅ Index RAG peuplé avec {count} documents")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du peuplement RAG: {e}")
        return False

def test_chatbot_query():
    """Test d'une requête chatbot avec RAG"""
    print("💬 Test d'une requête chatbot...")
    
    try:
        from apps.chatbot.core_chatbot import ParcInfoChatbot
        
        chatbot = ParcInfoChatbot()
        
        # Test d'une requête simple
        query = "Combien d'équipements informatiques avons-nous ?"
        print(f"Question: {query}")
        
        response = chatbot.process_query(query)
        print(f"Réponse: {response[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test chatbot: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Gestionnaire RAG ParcInfo")
    print("=" * 40)
    
    # Test du système RAG
    if test_rag():
        print("\n✅ Système RAG opérationnel")
        
        # Peupler l'index
        if populate_rag_index():
            print("\n✅ Index RAG peuplé")
            
            # Test du chatbot
            if test_chatbot_query():
                print("\n🎉 Tous les tests RAG sont réussis !")
            else:
                print("\n❌ Test chatbot échoué")
        else:
            print("\n❌ Peuplement de l'index RAG échoué")
    else:
        print("\n❌ Système RAG non opérationnel")
