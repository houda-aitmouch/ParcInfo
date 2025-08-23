#!/usr/bin/env python
import os
import sys
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

def test_rag_chatbot():
    """Test du chatbot avec RAG activé"""
    
    # URL du chatbot
    url = "http://127.0.0.1:8000/chatbot/process_query/"
    
    # Questions de test
    test_questions = [
        "Combien d'utilisateurs y a-t-il dans le système ?",
        "Liste les matériels informatiques",
        "Quels sont les fournisseurs disponibles ?",
        "Montre-moi les commandes récentes",
        "Y a-t-il des garanties qui expirent bientôt ?"
    ]
    
    print("🧪 Test du Chatbot avec RAG activé")
    print("=" * 50)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Question: {question}")
        
        try:
            # Envoyer la requête
            response = requests.post(url, json={
                'query': question,
                'user_id': 'test_user'
            }, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Réponse reçue ({len(data.get('response', ''))} caractères)")
                print(f"📊 Intent détecté: {data.get('intent', 'N/A')}")
                print(f"🎯 Confiance: {data.get('confidence', 0):.2f}")
                
                # Afficher un extrait de la réponse
                response_text = data.get('response', '')
                if response_text:
                    preview = response_text[:200] + "..." if len(response_text) > 200 else response_text
                    print(f"💬 Réponse: {preview}")
                else:
                    print("❌ Réponse vide")
                    
            else:
                print(f"❌ Erreur HTTP: {response.status_code}")
                print(f"📄 Contenu: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur de connexion: {e}")
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Test terminé")

if __name__ == '__main__':
    test_rag_chatbot()
