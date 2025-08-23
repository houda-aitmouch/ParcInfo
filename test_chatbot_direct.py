#!/usr/bin/env python3
"""
Script de test direct pour le chatbot sans passer par Django
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

from apps.chatbot.core_chatbot import ParcInfoChatbot

def test_users_queries():
    """Test des requêtes sur les utilisateurs"""
    print("Initialisation du chatbot...")
    chatbot = ParcInfoChatbot()
    
    test_queries = [
        "liste des utilisateurs",
        "liste des utilisatuers",  # Test avec faute de frappe
        "compte des utilisateurs",
        "nombre d'utilisateurs",
        "total des utilisateurs",
        "list users",
        "count users"
    ]
    
    print("=== Test des requêtes sur les utilisateurs ===\n")
    
    for query in test_queries:
        print(f"Question: {query}")
        print("-" * 50)
        
        try:
            response = chatbot.process_query(query)
            if isinstance(response, dict):
                print(f"Réponse: {response.get('response', 'Pas de réponse')}")
                print(f"Intent: {response.get('intent', 'N/A')}")
                print(f"Confidence: {response.get('confidence', 'N/A')}")
                print(f"Source: {response.get('source', 'N/A')}")
            else:
                print(f"Réponse: {response}")
        except Exception as e:
            print(f"Erreur: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    test_users_queries()
