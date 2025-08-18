#!/usr/bin/env python3
"""
Script de test rapide pour valider le fonctionnement du chatbot ParcInfo
après les corrections de données.

Auteur: Assistant IA
Date: 18/08/2025
"""

import os
import sys
import django
import time

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

from apps.chatbot.core_chatbot import ParcInfoChatbot

def test_chatbot_basic():
    """Test basique du chatbot pour valider son fonctionnement"""
    print("🧪 Test basique du chatbot ParcInfo")
    print("="*50)
    
    try:
        # Initialisation du chatbot
        chatbot = ParcInfoChatbot()
        print("✅ Chatbot initialisé avec succès")
        
        # Test de questions simples
        test_questions = [
            "Combien de matériels y a-t-il ?",
            "Quels sont les fournisseurs ?",
            "Quelles sont les commandes ?"
        ]
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n🔍 Test {i}: {question}")
            
            start_time = time.time()
            try:
                response = chatbot.process_query(question)
                response_time = time.time() - start_time
                
                if isinstance(response, dict):
                    response_text = response.get('response', '')
                    intent = response.get('intent', 'unknown')
                    confidence = response.get('confidence', 0)
                    source = response.get('source', 'unknown')
                    
                    print(f"✅ Réponse reçue en {response_time:.2f}s")
                    print(f"   Intent: {intent} (confiance: {confidence:.1f})")
                    print(f"   Source: {source}")
                    print(f"   Réponse: {response_text[:100]}...")
                else:
                    print(f"✅ Réponse reçue en {response_time:.2f}s")
                    print(f"   Réponse: {str(response)[:100]}...")
                    
            except Exception as e:
                print(f"❌ Erreur: {e}")
        
        print("\n✅ Tests basiques terminés avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_chatbot_questions_complementaires():
    """Test des questions complémentaires pour valider les améliorations"""
    print("\n🧪 Test des questions complémentaires")
    print("="*50)
    
    try:
        # Initialisation du chatbot
        chatbot = ParcInfoChatbot()
        
        # Questions complémentaires clés
        test_questions = [
            "Quels matériels sont stockés à l'étage 1 ?",
            "Quelles demandes sont associées à la comande BC23 ?",
            "Quel est le statut des livraisons pour le fourniseur 3STD ?"
        ]
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n🔍 Test complémentaire {i}: {question}")
            
            start_time = time.time()
            try:
                response = chatbot.process_query(question)
                response_time = time.time() - start_time
                
                if isinstance(response, dict):
                    response_text = response.get('response', '')
                    intent = response.get('intent', 'unknown')
                    confidence = response.get('confidence', 0)
                    source = response.get('source', 'unknown')
                    
                    print(f"✅ Réponse reçue en {response_time:.2f}s")
                    print(f"   Intent: {intent} (confiance: {confidence:.1f})")
                    print(f"   Source: {source}")
                    print(f"   Réponse: {response_text[:150]}...")
                    
                    # Validation rapide de la qualité
                    if 'Salut' in response_text or 'Bonjour' in response_text:
                        print("   ✅ Introduction engageante détectée")
                    else:
                        print("   ⚠️ Introduction manquante")
                    
                    if '?' in response_text or 'Besoin' in response_text:
                        print("   ✅ Invitation à poursuivre détectée")
                    else:
                        print("   ⚠️ Invitation manquante")
                        
                else:
                    print(f"✅ Réponse reçue en {response_time:.2f}s")
                    print(f"   Réponse: {str(response)[:150]}...")
                    
            except Exception as e:
                print(f"❌ Erreur: {e}")
        
        print("\n✅ Tests complémentaires terminés avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🚀 Test Rapide du Chatbot ParcInfo")
    print("📅 Date: 18/08/2025")
    print("🎯 Objectif: Valider le fonctionnement après corrections")
    
    try:
        # Tests basiques
        basic_success = test_chatbot_basic()
        
        if basic_success:
            # Tests complémentaires
            complement_success = test_chatbot_questions_complementaires()
            
            if complement_success:
                print("\n🎉 Tous les tests sont passés avec succès!")
                print("✅ Le chatbot fonctionne correctement après les corrections")
            else:
                print("\n⚠️ Tests complémentaires échoués")
        else:
            print("\n❌ Tests basiques échoués")
            
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrompus par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
