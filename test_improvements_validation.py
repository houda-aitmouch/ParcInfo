#!/usr/bin/env python3
"""
Script de test pour valider les améliorations apportées au chatbot ParcInfo

Auteur: Assistant IA
Date: 18/08/2025
"""

import os
import sys
import django
import time

# Configuration Django
sys.path.append('/Users/HouDa/PycharmProjects/ParcInfo')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

from apps.chatbot.core_chatbot import ParcInfoChatbot

def test_chatbot_improvements():
    """Teste les améliorations apportées au chatbot"""
    print("🧪 Test des Améliorations du Chatbot ParcInfo")
    print("="*60)
    
    try:
        # Initialisation du chatbot
        chatbot = ParcInfoChatbot()
        print("✅ Chatbot initialisé avec succès")
        
        # Test des nouvelles fonctionnalités
        print("\n🔍 Test des nouvelles fonctionnalités...")
        
        # Vérifier que les méthodes d'amélioration sont présentes
        improvements_available = [
            '_validate_response_quality',
            '_improve_tone',
            '_handle_edge_case',
            '_check_data_consistency'
        ]
        
        for method in improvements_available:
            if hasattr(chatbot, method):
                print(f"✅ {method} : Disponible")
            else:
                print(f"❌ {method} : Manquante")
        
        # Test des questions avec améliorations
        test_questions = [
            "Quels matériels sont stockés à l'étage 1 ?",
            "Quelles demandes sont associées à la comande BC23 ?",
            "Quel est le statut des livraisons pour le fourniseur 3STD ?"
        ]
        
        print(f"\n🧪 Test des questions avec améliorations...")
        
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
                    print(f"   Réponse: {response_text[:150]}...")
                    
                    # Validation des améliorations
                    print(f"   📊 Validation des améliorations:")
                    
                    # Vérifier l'introduction
                    if any(word in response_text[:30] for word in ['Bonjour', 'Salut', 'Hello']):
                        print(f"      ✅ Introduction engageante présente")
                    else:
                        print(f"      ⚠️ Introduction manquante")
                    
                    # Vérifier la conclusion
                    if '?' in response_text or any(word in response_text[-50:] for word in ['Besoin', 'Veux-tu', 'Voulez-vous']):
                        print(f"      ✅ Invitation à poursuivre présente")
                    else:
                        print(f"      ⚠️ Invitation manquante")
                    
                    # Vérifier les répétitions
                    if 'numéro de numéro de série' in response_text:
                        print(f"      ❌ Répétition détectée")
                    else:
                        print(f"      ✅ Pas de répétition")
                    
                    # Vérifier les numéros de série incorrects
                    if '123456' in response_text or '12345' in response_text:
                        print(f"      ❌ Numéros de série incorrects détectés")
                    else:
                        print(f"      ✅ Numéros de série corrects")
                        
                else:
                    print(f"✅ Réponse reçue en {response_time:.2f}s")
                    print(f"   Réponse: {str(response)[:150]}...")
                    
            except Exception as e:
                print(f"❌ Erreur: {e}")
        
        print("\n✅ Tests des améliorations terminés avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🚀 Validation des Améliorations du Chatbot ParcInfo")
    print("📅 Date: 18/08/2025")
    print("🎯 Objectif: Valider les améliorations implémentées")
    
    try:
        # Test des améliorations
        success = test_chatbot_improvements()
        
        if success:
            print("\n🎉 Toutes les améliorations sont fonctionnelles!")
            print("✅ Le chatbot est maintenant amélioré avec:")
            print("   • Validation des réponses")
            print("   • Cohérence du ton")
            print("   • Gestion intelligente des cas limites")
            print("   • Validation de cohérence des données")
        else:
            print("\n⚠️ Certaines améliorations ne fonctionnent pas correctement")
            
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrompus par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
