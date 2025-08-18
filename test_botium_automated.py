#!/usr/bin/env python3
"""
Script de test automatisé Botium-like pour le chatbot ParcInfo
Test des 9 questions identifiées comme nécessitant des améliorations
Focus : Précision ET ton humain selon le nouveau prompt
"""

import os
import sys
import django
from datetime import datetime
import time
import json

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

from apps.chatbot.core_chatbot import ParcInfoChatbot

class BotiumTestSuite:
    """Suite de tests automatisés pour évaluer la précision et le ton humain"""
    
    def __init__(self):
        self.chatbot = None
        self.test_results = []
        self.start_time = None
        
    def setup(self):
        """Initialise le chatbot et la suite de tests"""
        try:
            print("🚀 Initialisation de la suite de tests Botium...")
            self.chatbot = ParcInfoChatbot()
            print("✅ Chatbot initialisé avec succès")
            return True
        except Exception as e:
            print(f"❌ Erreur d'initialisation: {e}")
            return False
    
    def evaluate_precision(self, response: str, expected_elements: list) -> dict:
        """Évalue la précision de la réponse selon les éléments attendus"""
        score = 0
        found_elements = []
        missing_elements = []
        
        response_lower = response.lower()
        
        for element in expected_elements:
            if element.lower() in response_lower:
                score += 1
                found_elements.append(element)
            else:
                missing_elements.append(element)
        
        precision_score = score / len(expected_elements) if expected_elements else 0
        
        return {
            'score': precision_score,
            'found': found_elements,
            'missing': missing_elements,
            'is_accurate': precision_score >= 0.8
        }
    
    def evaluate_human_tone(self, response: str) -> dict:
        """Évalue le ton humain selon les directives du prompt"""
        score = 0
        issues = []
        improvements = []
        
        response_lower = response.lower()
        
        # Vérifier l'introduction engageante (directive 2 du prompt)
        if any(greeting in response_lower for greeting in ['bonjour', 'salut', 'j\'ai vérifié', 'j\'ai trouvé']):
            score += 2
        else:
            issues.append("Manque d'introduction engageante")
            improvements.append("Ajouter 'Bonjour ! J'ai vérifié pour vous'")
        
        # Vérifier l'absence de termes techniques (directive 2 du prompt)
        technical_terms = ['it', 'cmd', 'fin', 'série', 'n/a']
        for term in technical_terms:
            if term in response_lower:
                score -= 1
                issues.append(f"Terme technique '{term}' présent")
                improvements.append(f"Remplacer '{term}' par un terme clair")
        
        # Vérifier l'invitation à poursuivre (directive 2 du prompt)
        if any(engagement in response_lower for engagement in ['voulez-vous', 'avez-vous', 'besoin', 'souhaitez-vous']):
            score += 2
        else:
            issues.append("Manque d'invitation à poursuivre")
            improvements.append("Ajouter une question d'engagement")
        
        # Vérifier la structure claire (directive 4 du prompt)
        if len(response.split('.')) > 2:
            score += 1
        else:
            issues.append("Structure de réponse trop simple")
            improvements.append("Structurer avec introduction, détails, conclusion")
        
        # Normaliser le score sur 5
        score = max(0, min(5, score))
        
        return {
            'score': score,
            'issues': issues,
            'improvements': improvements,
            'is_human': score >= 3
        }
    
    def run_single_test(self, test_name: str, query: str, expected_elements: list, timeout: int = 5) -> dict:
        """Exécute un test individuel"""
        print(f"\n🔍 Test : {test_name}")
        print(f"📝 Question : {query}")
        print("-" * 50)
        
        start_time = time.time()
        
        try:
            # Exécuter la requête avec timeout
            response = self.chatbot.process_query(query)
            response_time = time.time() - start_time
            
            # Extraire le texte de la réponse
            if isinstance(response, dict):
                response_text = response.get('response', 'N/A')
                intent = response.get('intent', 'N/A')
                confidence = response.get('confidence', 'N/A')
            else:
                response_text = response
                intent = 'N/A'
                confidence = 'N/A'
            
            # Évaluer la précision
            precision_eval = self.evaluate_precision(response_text, expected_elements)
            
            # Évaluer le ton humain
            tone_eval = self.evaluate_human_tone(response_text)
            
            # Vérifier le timeout
            timeout_ok = response_time < timeout
            
            # Résultats du test
            test_result = {
                'test_name': test_name,
                'query': query,
                'response': response_text,
                'intent': intent,
                'confidence': confidence,
                'response_time': response_time,
                'timeout_ok': timeout_ok,
                'precision': precision_eval,
                'tone': tone_eval,
                'overall_score': (precision_eval['score'] + tone_eval['score'] / 5) / 2
            }
            
            # Affichage des résultats
            print(f"📝 Réponse : {response_text[:100]}{'...' if len(response_text) > 100 else ''}")
            print(f"🎯 Intent : {intent}")
            print(f"📊 Confiance : {confidence}%")
            print(f"⏱️  Temps : {response_time:.2f}s")
            print(f"📊 Précision : {precision_eval['score']:.2f} ({'✅' if precision_eval['is_accurate'] else '❌'})")
            print(f"🎭 Ton humain : {tone_eval['score']}/5 ({'✅' if tone_eval['is_human'] else '❌'})")
            
            if precision_eval['missing']:
                print(f"⚠️  Éléments manquants : {', '.join(precision_eval['missing'])}")
            
            if tone_eval['issues']:
                print(f"⚠️  Problèmes de ton : {', '.join(tone_eval['issues'])}")
            
            if not timeout_ok:
                print(f"⚠️  Timeout dépassé ({response_time:.2f}s > {timeout}s)")
            
            return test_result
            
        except Exception as e:
            print(f"❌ Erreur lors du test : {e}")
            return {
                'test_name': test_name,
                'query': query,
                'error': str(e),
                'overall_score': 0
            }
    
    def run_test_suite(self):
        """Exécute la suite complète de tests"""
        if not self.setup():
            return False
        
        print("\n🧪 Démarrage de la suite de tests automatisés")
        print("=" * 60)
        
        self.start_time = datetime.now()
        
        # Définition des tests avec éléments attendus
        test_cases = [
            {
                'name': 'Matériels pour superadmin avec demandes',
                'query': "Quel matériel a été affecté à la demande de 'superadmin' ?",
                'expected': ['Demande n°', 'cd14', 'sn14', 'BC23', 'Caméra', 'Casque', 'Baie']
            },
            {
                'name': 'Matériels informatiques sous garantie (détails)',
                'query': "Quels matériels informatiques sont encore sous garantie ?",
                'expected': ['cd12', 'cd13', 'cd14', 'ADD/INFO/010', 'designation', 'utilisateur', 'numéro de série']
            },
            {
                'name': 'Garantie ADD/INFO/01094 (détails)',
                'query': "La garantie du matériel avec le code d'inventaire ADD/INFO/01094 est-elle toujours active ?",
                'expected': ['ADD/INFO/01094', 'AOO2025', 'Armoire', 'jours restants', '28/07/2026']
            },
            {
                'name': 'Matériels bureautiques expirant bientôt (contexte)',
                'query': "Liste les matériels bureautiques dont la garantie expire bientôt.",
                'expected': ['30 jours', 'matériels actifs', 'contexte', 'ADD/INFO/01094']
            },
            {
                'name': 'Codes d\'inventaire Baie (utilisateurs)',
                'query': "Quel est le code d'inventaire de la Baie ?",
                'expected': ['cd12', 'cd13', 'cd14', 'utilisateur', 'employe anonyme', 'gestionnaire bureau', 'superadmin']
            },
            {
                'name': 'Commandes sans garantie (dates)',
                'query': "Y a-t-il des commandes sans garantie spécifiée ?",
                'expected': ['AOO2025', '123', 'BC23', 'expire', '28/07/2026', '15/09/2025', '23/08/2025']
            },
            {
                'name': 'Commandes bureautiques garantie années (conversationnel)',
                'query': "Liste des commandes bureautiques avec garantie en années.",
                'expected': ['AOO2025', '1 an', '28/07/2026', 'active', 'conversationnel']
            },
            {
                'name': 'Types de matériels (designations spécifiques)',
                'query': "Quels types de matériels sont disponibles ?",
                'expected': ['Baie', 'Call Server', 'Armoire', 'Câble', 'cd12', 'cd13', 'cd14', 'ADD/INFO/010']
            },
            {
                'name': 'Matériel sn12 avec garantie (détails)',
                'query': "Quel matériel informatique avec le numéro de série sn12 a une garantie associée ?",
                'expected': ['cd12', 'BC23', '23/08/2025', 'jours restants', '5 jours']
            },
            {
                'name': 'Matériels superadmin sous garantie (détails)',
                'query': "Y a-t-il des matériels affectés à 'superadmin' encore sous garantie ?",
                'expected': ['cd14', 'sn14', 'Baie', '23/08/2025', '5 jours restants', 'BC23']
            }
        ]
        
        # Exécution des tests
        for test_case in test_cases:
            result = self.run_single_test(
                test_case['name'],
                test_case['query'],
                test_case['expected']
            )
            self.test_results.append(result)
        
        # Génération du rapport
        self.generate_report()
        
        return True
    
    def generate_report(self):
        """Génère un rapport détaillé des tests"""
        print("\n📊 RAPPORT FINAL DES TESTS")
        print("=" * 60)
        
        if not self.test_results:
            print("❌ Aucun résultat de test disponible")
            return
        
        # Calcul des statistiques
        total_tests = len(self.test_results)
        successful_tests = len([r for r in self.test_results if 'error' not in r])
        failed_tests = total_tests - successful_tests
        
        # Scores moyens
        precision_scores = [r['precision']['score'] for r in self.test_results if 'precision' in r]
        tone_scores = [r['tone']['score'] for r in self.test_results if 'tone' in r]
        overall_scores = [r['overall_score'] for r in self.test_results if 'overall_score' in r]
        
        avg_precision = sum(precision_scores) / len(precision_scores) if precision_scores else 0
        avg_tone = sum(tone_scores) / len(tone_scores) if tone_scores else 0
        avg_overall = sum(overall_scores) / len(overall_scores) if overall_scores else 0
        
        # Temps de réponse
        response_times = [r['response_time'] for r in self.test_results if 'response_time' in r]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        max_response_time = max(response_times) if response_times else 0
        
        # Affichage des statistiques
        print(f"📈 Statistiques générales :")
        print(f"   • Tests exécutés : {total_tests}")
        print(f"   • Tests réussis : {successful_tests}")
        print(f"   • Tests échoués : {failed_tests}")
        print(f"   • Taux de succès : {(successful_tests/total_tests)*100:.1f}%")
        
        print(f"\n📊 Scores moyens :")
        print(f"   • Précision : {avg_precision:.2f}/1.0")
        print(f"   • Ton humain : {avg_tone:.1f}/5.0")
        print(f"   • Score global : {avg_overall:.2f}/1.0")
        
        print(f"\n⏱️  Performance :")
        print(f"   • Temps de réponse moyen : {avg_response_time:.2f}s")
        print(f"   • Temps de réponse max : {max_response_time:.2f}s")
        
        # Résultats par test
        print(f"\n🔍 Résultats détaillés par test :")
        for i, result in enumerate(self.test_results, 1):
            status = "✅" if result.get('overall_score', 0) >= 0.7 else "❌"
            print(f"   {i}. {result['test_name']} : {status} (Score: {result.get('overall_score', 0):.2f})")
        
        # Recommandations
        print(f"\n💡 Recommandations :")
        if avg_precision < 0.8:
            print("   • Améliorer la précision : inclure tous les détails attendus")
        if avg_tone < 3:
            print("   • Améliorer le ton humain : ajouter introductions et engagements")
        if avg_response_time > 2:
            print("   • Optimiser les performances : réduire le temps de réponse")
        
        # Sauvegarde du rapport
        self.save_report()
    
    def save_report(self):
        """Sauvegarde le rapport au format JSON"""
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'test_results': self.test_results,
            'summary': {
                'total_tests': len(self.test_results),
                'successful_tests': len([r for r in self.test_results if 'error' not in r]),
                'failed_tests': len([r for r in self.test_results if 'error' in r])
            }
        }
        
        filename = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Rapport sauvegardé : {filename}")
        except Exception as e:
            print(f"\n⚠️  Erreur lors de la sauvegarde : {e}")

def main():
    """Fonction principale"""
    print("🤖 Suite de tests Botium pour le chatbot ParcInfo")
    print("Focus : Précision ET ton humain selon le nouveau prompt")
    print("=" * 60)
    
    # Créer et exécuter la suite de tests
    test_suite = BotiumTestSuite()
    success = test_suite.run_test_suite()
    
    if success:
        print("\n🎉 Suite de tests terminée avec succès !")
    else:
        print("\n❌ Suite de tests échouée !")
    
    return success

if __name__ == "__main__":
    main()
