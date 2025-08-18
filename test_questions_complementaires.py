#!/usr/bin/env python3
"""
Script de test automatisé pour les 10 questions complémentaires du chatbot ParcInfo
Cible : Précision, complétude, ton humain, robustesse face aux erreurs
Date : 18/08/2025, 21:30 +01
"""

import os
import sys
import django
from datetime import datetime
import time

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

from apps.chatbot.core_chatbot import ParcInfoChatbot

class TestQuestionsComplementaires:
    """Test des 10 questions complémentaires pour valider les améliorations"""
    
    def __init__(self):
        print("🧪 Test des Questions Complémentaires du Chatbot ParcInfo")
        print("=" * 60)
        print("Focus : Précision, Complétude, Ton Humain, Robustesse")
        print("Date : 18/08/2025, 21:30 +01")
        print()
        
        try:
            self.chatbot = ParcInfoChatbot()
            print("✅ Chatbot initialisé avec succès")
        except Exception as e:
            print(f"❌ Erreur d'initialisation : {e}")
            sys.exit(1)
    
    def evaluate_response_quality(self, response: str, expected_keywords: list, 
                                expected_absence: list = None) -> dict:
        """Évalue la qualité de la réponse"""
        if expected_absence is None:
            expected_absence = []
        
        # Vérification des mots-clés attendus
        keywords_found = []
        for keyword in expected_keywords:
            if keyword.lower() in response.lower():
                keywords_found.append(keyword)
        
        # Vérification de l'absence de mots non désirés
        unwanted_found = []
        for word in expected_absence:
            if word.lower() in response.lower():
                unwanted_found.append(word)
        
        # Score de précision
        precision_score = len(keywords_found) / len(expected_keywords) if expected_keywords else 0
        
        # Score de ton humain
        human_indicators = [
            'bonjour', 'salut', 'excellent', 'parfait', 'super',
            'veux-tu', 'besoin', 'désolé', 'désolée', 'merci'
        ]
        human_score = sum(1 for indicator in human_indicators if indicator in response.lower()) / len(human_indicators)
        
        return {
            'precision_score': precision_score,
            'keywords_found': keywords_found,
            'missing_keywords': [k for k in expected_keywords if k not in keywords_found],
            'unwanted_found': unwanted_found,
            'human_score': human_score,
            'response_length': len(response)
        }
    
    def test_question(self, question: str, expected_keywords: list, 
                      expected_absence: list = None, description: str = "") -> dict:
        """Teste une question spécifique"""
        print(f"🔍 Question : {question}")
        if description:
            print(f"📋 Description : {description}")
        print("-" * 50)
        
        start_time = time.time()
        try:
            response = self.chatbot.process_query(question)
            response_time = time.time() - start_time
        except Exception as e:
            response = f"Erreur : {e}"
            response_time = 0
        
        # Gérer les réponses dict vs string
        response_text = response.get('response', str(response)) if isinstance(response, dict) else str(response)
        
        print(f"📝 Réponse : {response_text}")
        print(f"⏱️  Temps : {response_time:.2f}s")
        
        # Évaluation de la qualité
        quality = self.evaluate_response_quality(response_text, expected_keywords, expected_absence)
        
        print(f"🎯 Score précision : {quality['precision_score']:.1%}")
        print(f"✅ Mots-clés trouvés : {', '.join(quality['keywords_found'])}")
        if quality['missing_keywords']:
            print(f"❌ Mots-clés manquants : {', '.join(quality['missing_keywords'])}")
        if quality['unwanted_found']:
            print(f"⚠️  Mots non désirés : {', '.join(quality['unwanted_found'])}")
        print(f"🎭 Score ton humain : {quality['human_score']:.1%}")
        print(f"📏 Longueur réponse : {quality['response_length']} caractères")
        
        # Vérification performance
        if response_time > 2.0:
            print("⚠️  Performance : Réponse lente (>2s)")
        else:
            print("✅ Performance : Réponse rapide (<2s)")
        
        print()
        return {
            'question': question,
            'response': response,
            'response_time': response_time,
            'quality': quality
        }
    
    def run_all_tests(self):
        """Exécute tous les tests des questions complémentaires"""
        print("📋 Test de 10 questions complémentaires")
        print("Cible : Lacunes identifiées (précision, complétude, ton, robustesse)")
        print("-" * 50)
        print()
        
        test_cases = [
            {
                'question': "Quelles sont les demandes en attente pour superadmin ?",
                'expected_keywords': ['aucune demande', 'n°11', 'n°21', 'n°23', 'approuvées'],
                'expected_absence': ['en attente'],
                'description': "Vérifier absence de demandes en attente et liste des demandes approuvées"
            },
            {
                'question': "Quel est le fourniseur de la comande BC23 ?",
                'expected_keywords': ['TECHNICOVIGILE', 'BC23', 'cd12', 'cd13', 'cd14'],
                'expected_absence': ['fourniseur', 'comande'],
                'description': "Tester robustesse face aux fautes d'orthographe et précision des données"
            },
            {
                'question': "Quels matériels ont été livrés après la date prévue ?",
                'expected_keywords': ['retard', 'BC23', '123', 'AOO2025', 'cd12', 'cd13', 'cd14'],
                'description': "Vérifier la gestion des retards de livraison et la précision des dates"
            },
            {
                'question': "Combien de matériels sont en maintenance actuellement ?",
                'expected_keywords': ['aucun matériel', 'maintenance', 'nouveaux', 'affectés'],
                'description': "Tester la gestion des cas vides et la fourniture de contexte"
            },
            {
                'question': "Quels matériels sont associés à la comande 123 ?",
                'expected_keywords': ['commande 123', 'ADD/INFO/010', 'ADD/INFO/01000', '15/09/2025'],
                'expected_absence': ['comande'],
                'description': "Vérifier la correction des fautes et la complétude des informations"
            },
            {
                'question': "Quel est le matériel avec le numéro de série 123456 ?",
                'expected_keywords': ['numéro de série 123456', 'incorrect', 'ADD/INFO/010'],
                'description': "Tester la gestion des données inexistantes et la fourniture d'alternatives"
            },
            {
                'question': "Quelles sont les commandes passées par le fourniseur AEBDM ?",
                'expected_keywords': ['AEBDM', 'AOO2025', 'ADD/INFO/01094', '28/07/2025'],
                'expected_absence': ['fourniseur'],
                'description': "Vérifier la gestion des fautes et la précision des relations fournisseur-commande"
            },
            {
                'question': "Combien de matériels informatiques sont affectés à un utilisateur ?",
                'expected_keywords': ['3 matériels', 'cd12', 'cd13', 'cd14', 'employe anonyme', 'gestionnaire bureau', 'superadmin'],
                'description': "Tester les statistiques et la complétude des informations utilisateur"
            },
            {
                'question': "Quels matériels ont une garantie de moins de 10 jours restants ?",
                'expected_keywords': ['moins de 10 jours', 'cd12', 'cd13', 'cd14', '5 jours restants', '23/08/2025'],
                'description': "Vérifier le calcul des jours restants et la précision des dates"
            },
            {
                'question': "Quel matériel est lié à la demande n°999 ?",
                'expected_keywords': ['demande n°999', 'n\'existe pas', 'n°11', 'n°21', 'n°23'],
                'description': "Tester la gestion des cas limites et la fourniture d'alternatives"
            }
        ]
        
        results = []
        for i, test_case in enumerate(test_cases, 1):
            print(f"📝 Test {i}/10")
            result = self.test_question(
                test_case['question'],
                test_case['expected_keywords'],
                test_case.get('expected_absence', []),
                test_case['description']
            )
            results.append(result)
        
        return results
    
    def generate_report(self, results: list):
        """Génère un rapport détaillé des tests"""
        print("🏁 Rapport des Tests Complémentaires")
        print("=" * 60)
        
        # Statistiques globales
        total_questions = len(results)
        avg_precision = sum(r['quality']['precision_score'] for r in results) / total_questions
        avg_human_score = sum(r['quality']['human_score'] for r in results) / total_questions
        avg_response_time = sum(r['response_time'] for r in results) / total_questions
        
        print(f"📊 Statistiques Globales :")
        print(f"   • Questions testées : {total_questions}")
        print(f"   • Score précision moyen : {avg_precision:.1%}")
        print(f"   • Score ton humain moyen : {avg_human_score:.1%}")
        print(f"   • Temps de réponse moyen : {avg_response_time:.2f}s")
        print()
        
        # Questions avec problèmes
        problematic_questions = [r for r in results if r['quality']['precision_score'] < 0.8 or r['quality']['human_score'] < 0.6]
        
        if problematic_questions:
            print("⚠️  Questions avec Problèmes :")
            print("-" * 40)
            for result in problematic_questions:
                print(f"   • {result['question'][:50]}...")
                if result['quality']['precision_score'] < 0.8:
                    print(f"     - Précision faible : {result['quality']['precision_score']:.1%}")
                if result['quality']['human_score'] < 0.6:
                    print(f"     - Ton non-humain : {result['quality']['human_score']:.1%}")
                if result['response_time'] > 2.0:
                    print(f"     - Performance lente : {result['response_time']:.2f}s")
            print()
        
        # Questions réussies
        successful_questions = [r for r in results if r['quality']['precision_score'] >= 0.8 and r['quality']['human_score'] >= 0.6 and r['response_time'] <= 2.0]
        
        if successful_questions:
            print("✅ Questions Réussies :")
            print("-" * 30)
            for result in successful_questions:
                print(f"   • {result['question'][:50]}...")
            print()
        
        # Recommandations
        print("💡 Recommandations :")
        print("-" * 20)
        
        if avg_precision < 0.8:
            print("   • Améliorer la précision des réponses (cible : >80%)")
        if avg_human_score < 0.6:
            print("   • Améliorer le ton humain (cible : >60%)")
        if avg_response_time > 2.0:
            print("   • Optimiser les performances (cible : <2s)")
        
        if problematic_questions:
            print("   • Revoir les questions problématiques identifiées")
        
        print("   • Continuer les tests avec variations et cas limites")
        print("   • Implémenter le feedback utilisateur (thumbs up/down)")
        
        return {
            'total_questions': total_questions,
            'avg_precision': avg_precision,
            'avg_human_score': avg_human_score,
            'avg_response_time': avg_response_time,
            'problematic_count': len(problematic_questions),
            'successful_count': len(successful_questions)
        }

def main():
    """Fonction principale"""
    try:
        tester = TestQuestionsComplementaires()
        results = tester.run_all_tests()
        report = tester.generate_report(results)
        
        print("🎯 Objectifs de Performance :")
        print(f"   • Précision >95% : {'✅ Atteint' if report['avg_precision'] >= 0.95 else '❌ Non atteint'} ({report['avg_precision']:.1%})")
        print(f"   • Ton humain CSAT >4/5 : {'✅ Atteint' if report['avg_human_score'] >= 0.8 else '❌ Non atteint'} ({report['avg_human_score']:.1%})")
        print(f"   • Performance <2s : {'✅ Atteint' if report['avg_response_time'] <= 2.0 else '❌ Non atteint'} ({report['avg_response_time']:.2f}s)")
        
        print("\n🚀 Test des questions complémentaires terminé !")
        
    except KeyboardInterrupt:
        print("\n⏹️  Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors du test : {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
