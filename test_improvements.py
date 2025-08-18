#!/usr/bin/env python3
"""
Script de test pour vérifier les améliorations du chatbot ParcInfo
Basé sur l'analyse des réponses du 18/08/2025, 20:16-20:17
Focus sur la précision ET le ton humain
"""

import os
import sys
import django
from datetime import datetime

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

from apps.chatbot.core_chatbot import ParcInfoChatbot

def evaluate_tone_human(response: str) -> dict:
    """Évalue si la réponse a un ton humain et conversationnel"""
    tone_score = 0
    tone_issues = []
    tone_improvements = []
    
    response_lower = response.lower()
    
    # Vérifier les éléments de ton humain
    if any(greeting in response_lower for greeting in ['bonjour', 'salut', 'voici', 'j\'ai trouvé', 'j\'ai vérifié']):
        tone_score += 2
    else:
        tone_issues.append("Manque d'introduction conviviale")
        tone_improvements.append("Ajouter 'Bonjour ! J'ai vérifié pour vous' ou similaire")
    
    if any(engagement in response_lower for engagement in ['voulez-vous', 'avez-vous', 'besoin', 'souhaitez-vous', 'n\'hésitez pas']):
        tone_score += 2
    else:
        tone_issues.append("Manque d'engagement conversationnel")
        tone_improvements.append("Ajouter une question d'engagement à la fin")
    
    if '?' in response:
        tone_score += 1
    else:
        tone_issues.append("Pas de question d'engagement")
    
    # Vérifier l'absence de termes techniques
    technical_terms = ['it', 'cmd', 'fin', 'série', 'n/a']
    for term in technical_terms:
        if term in response_lower:
            tone_score -= 1
            tone_issues.append(f"Terme technique '{term}' présent")
            tone_improvements.append(f"Remplacer '{term}' par un terme plus clair")
    
    # Vérifier la présence de phrases complètes
    if len(response.split('.')) > 2:
        tone_score += 1
    else:
        tone_issues.append("Réponse trop courte")
        tone_improvements.append("Développer avec plus de contexte")
    
    # Normaliser le score sur 5
    tone_score = max(0, min(5, tone_score))
    
    return {
        'score': tone_score,
        'issues': tone_issues,
        'improvements': tone_improvements,
        'is_human': tone_score >= 3
    }

def test_chatbot_improvements():
    """Test des améliorations du chatbot"""
    print("🧪 Test des améliorations du chatbot ParcInfo")
    print("=" * 60)
    
    # Initialiser le chatbot
    try:
        chatbot = ParcInfoChatbot()
        print("✅ Chatbot initialisé avec succès")
    except Exception as e:
        print(f"❌ Erreur d'initialisation: {e}")
        return
    
    # Questions à tester (basées sur l'analyse)
    test_questions = [
        # 1. Matériels pour superadmin (avec demandes)
        "Quel matériel a été affecté à la demande de 'superadmin' ?",
        
        # 2. Fourniture cable (déjà correct)
        "Quel est le numéro de série de la fourniture 'cable' ?",
        
        # 3. Matériels informatiques sous garantie (avec détails)
        "Quels matériels informatiques sont encore sous garantie ?",
        
        # 4. Garantie ADD/INFO/01094 (avec designation et jours)
        "La garantie du matériel avec le code d'inventaire ADD/INFO/01094 est-elle toujours active ?",
        
        # 5. Matériels bureautiques expirant bientôt (avec contexte)
        "Liste les matériels bureautiques dont la garantie expire bientôt.",
        
        # 6. Codes d'inventaire Baie (avec utilisateurs)
        "Quel est le code d'inventaire de la Baie ?",
        
        # 7. Commandes sans garantie (avec dates d'expiration)
        "Y a-t-il des commandes sans garantie spécifiée ?",
        
        # 8. Commandes bureautiques avec garantie en années (déjà correct)
        "Liste des commandes bureautiques avec garantie en années.",
        
        # 9. Types de matériels (avec designations spécifiques)
        "Quels types de matériels sont disponibles ?",
        
        # 10. Matériel sn12 avec garantie (avec code et jours)
        "Quel matériel informatique avec le numéro de série sn12 a une garantie associée ?",
        
        # 11. Matériels superadmin sous garantie (avec détails)
        "Y a-t-il des matériels affectés à 'superadmin' encore sous garantie ?"
    ]
    
    print(f"\n📋 Test de {len(test_questions)} questions améliorées")
    print("Focus : Précision ET ton humain")
    print("-" * 60)
    
    total_accuracy_score = 0
    total_tone_score = 0
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n🔍 Question {i}: {question}")
        print("-" * 40)
        
        try:
            # Traiter la question
            start_time = datetime.now()
            response = chatbot.process_query(question)
            end_time = datetime.now()
            
            # Afficher la réponse
            if isinstance(response, dict):
                response_text = response.get('response', 'N/A')
                print(f"📝 Réponse: {response_text}")
                print(f"🎯 Intent: {response.get('intent', 'N/A')}")
                print(f"📊 Confiance: {response.get('confidence', 'N/A')}%")
            else:
                response_text = response
                print(f"📝 Réponse: {response}")
            
            # Temps de réponse
            response_time = (end_time - start_time).total_seconds()
            print(f"⏱️  Temps: {response_time:.2f}s")
            
            # Évaluation du ton humain
            tone_eval = evaluate_tone_human(response_text)
            print(f"🎭 Ton humain: {tone_eval['score']}/5 ({'✅ Humain' if tone_eval['is_human'] else '❌ Mécanique'})")
            
            if tone_eval['issues']:
                print(f"⚠️  Problèmes de ton: {', '.join(tone_eval['issues'])}")
            
            if tone_eval['improvements']:
                print(f"💡 Améliorations suggérées: {', '.join(tone_eval['improvements'])}")
            
            # Vérifications spécifiques de précision
            accuracy_score = 0
            accuracy_issues = []
            
            if i == 1:  # Matériels superadmin
                if "Demande n°" in response_text:
                    accuracy_score += 2
                    print("✅ Inclut les demandes spécifiques")
                else:
                    accuracy_issues.append("Manque les demandes spécifiques")
                    
            elif i == 3:  # Matériels informatiques sous garantie
                if "designation" in response_text.lower() or "utilisateur" in response_text.lower():
                    accuracy_score += 2
                    print("✅ Inclut les détails (designation, utilisateur)")
                else:
                    accuracy_issues.append("Manque les détails")
                    
            elif i == 4:  # ADD/INFO/01094
                if "designation" in response_text.lower() and "jours restants" in response_text.lower():
                    accuracy_score += 2
                    print("✅ Inclut designation et jours restants")
                else:
                    accuracy_issues.append("Manque designation ou jours restants")
                    
            elif i == 9:  # Types de matériels
                if "Baie" in response_text or "Call Server" in response_text or "Armoire" in response_text:
                    accuracy_score += 2
                    print("✅ Inclut les designations spécifiques")
                else:
                    accuracy_issues.append("Réponse trop générique")
                    
            elif i == 10:  # sn12
                if "cd12" in response_text and "jours restants" in response_text:
                    accuracy_score += 2
                    print("✅ Inclut code d'inventaire et jours restants")
                else:
                    accuracy_issues.append("Manque code d'inventaire ou jours restants")
            
            # Score de précision (0-2)
            accuracy_score = min(2, accuracy_score)
            total_accuracy_score += accuracy_score
            total_tone_score += tone_eval['score']
            
            print(f"📊 Score précision: {accuracy_score}/2")
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
        
        print()
    
    # Résumé final
    print("🏁 Résumé des tests")
    print("=" * 60)
    print(f"📊 Score précision moyen: {total_accuracy_score/len(test_questions):.1f}/2")
    print(f"🎭 Score ton humain moyen: {total_tone_score/len(test_questions):.1f}/5")
    
    overall_score = (total_accuracy_score/len(test_questions) + total_tone_score/len(test_questions)) / 2
    print(f"🌟 Score global: {overall_score:.1f}/3.5")
    
    if overall_score >= 2.5:
        print("🎉 Excellent ! Le chatbot est précis ET humain")
    elif overall_score >= 1.5:
        print("👍 Bien ! Quelques améliorations mineures nécessaires")
    else:
        print("⚠️  Des améliorations importantes sont nécessaires")

if __name__ == "__main__":
    test_chatbot_improvements()
