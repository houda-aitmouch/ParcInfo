#!/usr/bin/env python3
"""
Test Final des Questions Complémentaires avec Améliorations Appliquées
Valide que les améliorations (introduction, ton, invitation) sont visibles dans les réponses
"""

import sys
import os
import time
from datetime import datetime

# Ajouter le chemin du projet
sys.path.append('/Users/HouDa/PycharmProjects/ParcInfo')

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
import django
django.setup()

from apps.chatbot.core_chatbot import get_chatbot

def test_questions_complementaires():
    """Test des 10 questions complémentaires avec validation des améliorations"""
    
    print("🚀 Test Final des Questions Complémentaires")
    print("📅 Date:", datetime.now().strftime("%d/%m/%Y"))
    print("🎯 Objectif: Valider les améliorations appliquées")
    print("=" * 60)
    
    # Initialiser le chatbot
    print("Initializing ParcInfo Chatbot...")
    chatbot = get_chatbot()
    print("✅ Chatbot initialisé avec succès\n")
    
    # Questions complémentaires à tester
    questions = [
        "Quels matériels sont stockés à l'étage 1 ?",
        "Quelles demandes sont associées à la comande BC23 ?",
        "Quel est le statut des livraisons pour le fourniseur 3STD ?",
        "Quels matériels informatiques sont marqués comme nouveaux ?",
        "Quel est le total des comandes passées en juillet 2025 ?",
        "Quels matériels sont liés à des demandes non approuvées ?",
        "Quel fourniseur a livré le matériel ADD/INFO/01094 ?",
        "Quels matériels sont publics à l'étage 1 ?",
        "Combien de matériels sont en stock actuellement ?",
        "Quel matériel est associé au fourniseur INCONNU ?"
    ]
    
    scores = {
        'introduction': 0,
        'invitation': 0,
        'ton_ameliore': 0,
        'precision': 0,
        'performance': 0
    }
    
    total_questions = len(questions)
    
    for i, question in enumerate(questions, 1):
        print(f"🔍 Test {i}: {question}")
        
        # Mesurer le temps de réponse
        start_time = time.time()
        try:
            response = chatbot.process_query(question)
            response_time = time.time() - start_time
        except Exception as e:
            print(f"❌ Erreur: {e}")
            continue
        
        print(f"✅ Réponse reçue en {response_time:.2f}s")
        
        # Extraire le texte de la réponse
        if isinstance(response, dict) and 'response' in response:
            response_text = response['response']
        else:
            response_text = str(response)
        
        print(f"   Réponse: {response_text[:200]}...")
        
        # Validation des améliorations
        validation = validate_improvements(response_text, response_time)
        
        # Mise à jour des scores
        for key in scores:
            if validation[key]:
                scores[key] += 1
        
        print(f"   📊 Validation:")
        print(f"      {'✅' if validation['introduction'] else '⚠️'} Introduction présente")
        print(f"      {'✅' if validation['invitation'] else '⚠️'} Invitation présente")
        print(f"      {'✅' if validation['ton_ameliore'] else '⚠️'} Ton amélioré")
        print(f"      {'✅' if validation['precision'] else '⚠️'} Précision")
        print(f"      {'✅' if validation['performance'] else '⚠️'} Performance <2s")
        print()
    
    # Calcul des scores finaux
    print("📊 RÉSULTATS FINAUX")
    print("=" * 60)
    
    for key, score in scores.items():
        percentage = (score / total_questions) * 100
        status = "✅" if percentage >= 80 else "⚠️" if percentage >= 60 else "❌"
        print(f"{status} {key.replace('_', ' ').title()}: {score}/{total_questions} ({percentage:.1f}%)")
    
    # Score global
    global_score = sum(scores.values()) / (len(scores) * total_questions) * 100
    print(f"\n🎯 Score Global: {global_score:.1f}%")
    
    if global_score >= 80:
        print("🎉 Excellent ! Les améliorations sont pleinement appliquées !")
    elif global_score >= 60:
        print("✅ Bon ! Les améliorations sont majoritairement appliquées.")
    else:
        print("⚠️ Améliorations partielles. Vérification nécessaire.")
    
    return global_score

def validate_improvements(response, response_time):
    """Valide la présence des améliorations dans la réponse"""
    
    validation = {
        'introduction': False,
        'invitation': False,
        'ton_ameliore': False,
        'precision': False,
        'performance': False
    }
    
    # Vérifier l'introduction
    intro_phrases = ['bonjour', 'salut', 'parfait', 'excellent', 'super']
    validation['introduction'] = any(phrase in response.lower() for phrase in intro_phrases)
    
    # Vérifier l'invitation
    invitation_phrases = ['veux-tu', 'besoin', 'souhaitez', 'détails', 'plus d\'infos']
    validation['invitation'] = any(phrase in response.lower() for phrase in invitation_phrases)
    
    # Vérifier le ton amélioré (pas de répétitions, phrases naturelles)
    validation['ton_ameliore'] = (
        'numéro de numéro de série' not in response and
        'super !' not in response and
        'parfait !' not in response and
        len(response.split()) > 10  # Réponse suffisamment détaillée
    )
    
    # Vérifier la précision (pas d'erreurs évidentes)
    validation['precision'] = (
        '123456' not in response and
        '12345' not in response and
        'étage 2' not in response or 'ADD/INFO/01094' not in response
    )
    
    # Vérifier la performance
    validation['performance'] = response_time < 2.0
    
    return validation

if __name__ == "__main__":
    try:
        score = test_questions_complementaires()
        sys.exit(0 if score >= 60 else 1)
    except Exception as e:
        print(f"❌ Erreur critique: {e}")
        sys.exit(1)
