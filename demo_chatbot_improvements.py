#!/usr/bin/env python3
"""
Démonstration des améliorations du chatbot ParcInfo
"""

import os
import sys
import django
from datetime import datetime

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

from apps.chatbot.core_chatbot import get_chatbot, ResponseEnhancer

def demo_improvements():
    """Démonstration des améliorations"""
    print("🎭 DÉMONSTRATION DES AMÉLIORATIONS DU CHATBOT")
    print("=" * 60)
    
    # Test de la classe ResponseEnhancer
    print("\n🔧 TEST DE LA CLASSE RESPONSE ENHANCER")
    print("-" * 40)
    
    templates = {
        'intro_phrases': ["Voici la liste demandée :", "J'ai trouvé ces informations pour vous :"],
        'follow_up_questions': {
            'list_users': ["Voulez-vous modifier un rôle utilisateur ?", "Souhaitez-vous voir les permissions ?"],
            'list_materials': ["Voulez-vous voir les détails d'un matériel ?", "Souhaitez-vous vérifier la garantie ?"]
        },
        'correction_confirmations': ["J'ai corrigé automatiquement votre recherche.", "J'ai ajusté votre requête pour améliorer la recherche."],
        'humor_touches': ["😊", "👍", "💡", "✨"]
    }
    
    enhancer = ResponseEnhancer(templates)
    
    # Test 1: Réponse simple
    print("\n📝 Test 1: Réponse simple")
    print("Question: 'Liste des utilisateurs'")
    
    original_response = """**Liste des utilisateurs :**
• user1 — Actif
• user2 — Inactif"""
    
    enhanced = enhancer.enhance_response(
        original_response,
        intent='list_users',
        original_query='liste utilisateurs',
        corrected_query='liste utilisateurs'
    )
    
    print(f"\nRéponse originale:\n{original_response}")
    print(f"\nRéponse améliorée:\n{enhanced}")
    
    # Test 2: Avec correction
    print("\n📝 Test 2: Avec correction de faute de frappe")
    print("Question: 'Matereils bureau'")
    
    enhanced_with_correction = enhancer.enhance_response(
        original_response,
        intent='list_materials',
        original_query='matereils',
        corrected_query='matériels'
    )
    
    print(f"\nRéponse avec correction:\n{enhanced_with_correction}")
    
    # Test avec le vrai chatbot
    print("\n🤖 TEST AVEC LE VRAI CHATBOT")
    print("-" * 40)
    
    chatbot = get_chatbot()
    
    # Test des handlers améliorés
    test_cases = [
        {
            'query': 'Liste des utilisateurs',
            'description': 'Handler amélioré avec engagement'
        },
        {
            'query': 'Matériels à l\'étage 2',
            'description': 'Handler amélioré avec localisation'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test_case['description']}")
        print(f"Question: '{test_case['query']}'")
        
        try:
            result = chatbot.process_query(test_case['query'])
            
            if isinstance(result, dict):
                response = result.get('response', 'Erreur')
                intent = result.get('intent', 'unknown')
                
                print(f"\nIntent détecté: {intent}")
                print(f"Réponse:\n{response}")
                
                # Vérifier les améliorations
                improvements = []
                if any(phrase in response for phrase in ["Voici la liste demandée", "J'ai trouvé ces informations"]):
                    improvements.append("✅ Phrase d'intro engageante")
                
                if "💭 Question de suivi" in response:
                    improvements.append("✅ Question de suivi")
                
                if any(emoji in response for emoji in ["😊", "👍", "💡", "✨"]):
                    improvements.append("✅ Touche d'humour")
                
                if improvements:
                    print(f"\n🎉 Améliorations détectées:")
                    for improvement in improvements:
                        print(f"  {improvement}")
                else:
                    print(f"\n⚠️ Aucune amélioration détectée")
                    
            else:
                print(f"❌ Format de réponse inattendu")
                
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    print(f"\n" + "=" * 60)
    print("🎯 RÉSUMÉ DES AMÉLIORATIONS")
    print("=" * 60)
    
    improvements_summary = """
✅ AMÉLIORATIONS IMPLÉMENTÉES :

1. 🎭 PERSONNALITÉ ENGAGEANTE
   • Phrases d'introduction variées
   • Émojis et touches d'humour
   • Ton conversationnel et chaleureux

2. 🔧 GESTION DES ERREURS
   • Confirmation des corrections automatiques
   • Messages explicites pour les ajustements
   • Suggestions d'amélioration

3. 💬 INTERACTIVITÉ
   • Questions de suivi contextuelles
   • Suggestions d'actions suivantes
   • Engagement continu avec l'utilisateur

4. 🎛️ INTERFACE AMÉLIORÉE
   • Export PDF des réponses
   • Export CSV des données
   • Filtrage des résultats
   • Feedback utilisateur (thumbs up/down)
   • Copie améliorée avec feedback visuel

5. 🏗️ ARCHITECTURE MODULAIRE
   • Classe ResponseEnhancer réutilisable
   • Templates de conversation configurables
   • Système de feedback pour amélioration continue
   • Tests automatisés

📊 IMPACT ATTENDU :
• Expérience utilisateur plus naturelle et engageante
• Meilleure compréhension des corrections automatiques
• Plus d'options de manipulation des données
• Feedback visuel pour toutes les actions
• Code plus maintenable et extensible
"""
    
    print(improvements_summary)

if __name__ == "__main__":
    print("🚀 Démarrage de la démonstration des améliorations")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        demo_improvements()
        print("\n✅ Démonstration terminée avec succès!")
    except Exception as e:
        print(f"\n❌ Erreur lors de la démonstration: {e}")
        sys.exit(1)
