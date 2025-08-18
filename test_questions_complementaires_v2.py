#!/usr/bin/env python3
"""
Script de test pour valider les améliorations du chatbot ParcInfo
avec les 10 questions complémentaires ciblant les lacunes identifiées.

Auteur: Assistant IA
Date: 18/08/2025
Version: 2.0
"""

import os
import sys
import django
import time
import json
from datetime import datetime
from typing import Dict, List, Any, Tuple

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

from apps.chatbot.core_chatbot import ParcInfoChatbot
from apps.chatbot.models import ChatbotFeedback, IntentExample
from apps.materiel_informatique.models import MaterielInformatique
from apps.materiel_bureautique.models import MaterielBureau
from apps.commande_informatique.models import Commande
from apps.commande_bureau.models import CommandeBureau
from apps.fournisseurs.models import Fournisseur
from apps.users.models import CustomUser
from apps.livraison.models import Livraison
from apps.demande_equipement.models import DemandeEquipement

class ChatbotTesterV2:
    """Classe de test avancée pour le chatbot ParcInfo"""
    
    def __init__(self):
        """Initialise le testeur avec le chatbot et les données de référence"""
        self.chatbot = ParcInfoChatbot()
        self.test_results = []
        self.start_time = time.time()
        
        # Données de référence pour validation
        self.reference_data = self._load_reference_data()
        
        print("🚀 Initialisation du testeur de chatbot ParcInfo v2.0")
        print(f"📊 Données de référence chargées: {len(self.reference_data)} entités")
    
    def _load_reference_data(self) -> Dict[str, Any]:
        """Charge les données de référence depuis la base de données"""
        try:
            data = {
                'materiels': {},
                'commandes': {},
                'fournisseurs': {},
                'demandes': {},
                'utilisateurs': {}
            }
            
            # Matériels informatiques
            for mat in MaterielInformatique.objects.all():
                data['materiels'][mat.code_inventaire] = {
                    'type': 'informatique',
                    'numero_serie': mat.numero_serie,
                    'designation': mat.designation,
                    'utilisateur': mat.utilisateur.username if mat.utilisateur else None,
                    'commande_id': mat.commande.id if mat.commande else None,
                    'lieu_stockage': getattr(mat, 'lieu_stockage', 'etage1'),
                    'statut': getattr(mat, 'statut', 'affecte')
                }
            
            # Matériels bureautiques
            for mat in MaterielBureau.objects.all():
                data['materiels'][mat.code_inventaire] = {
                    'type': 'bureautique',
                    'numero_serie': mat.numero_serie,
                    'designation': mat.designation,
                    'utilisateur': mat.utilisateur.username if mat.utilisateur else None,
                    'commande_id': mat.commande.id if mat.commande else None,
                    'lieu_stockage': getattr(mat, 'lieu_stockage', 'etage1'),
                    'statut': getattr(mat, 'statut', 'affecte')
                }
            
            # Commandes
            for cmd in Commande.objects.all():
                data['commandes'][cmd.id] = {
                    'type': 'informatique',
                    'montant': float(cmd.montant),
                    'fournisseur': cmd.fournisseur.nom if cmd.fournisseur else None,
                    'date_commande': cmd.date_commande.strftime('%d/%m/%Y'),
                    'garantie_fin': cmd.garantie_fin.strftime('%d/%m/%Y') if cmd.garantie_fin else None
                }
            
            for cmd in CommandeBureau.objects.all():
                data['commandes'][cmd.id] = {
                    'type': 'bureautique',
                    'montant': float(cmd.montant),
                    'fournisseur': cmd.fournisseur.nom if cmd.fournisseur else None,
                    'date_commande': cmd.date_commande.strftime('%d/%m/%Y'),
                    'garantie_fin': cmd.garantie_fin.strftime('%d/%m/%Y') if cmd.garantie_fin else None
                }
            
            # Fournisseurs
            for four in Fournisseur.objects.all():
                data['fournisseurs'][four.nom] = {
                    'ice': four.ice,
                    'localisation': four.localisation
                }
            
            # Demandes
            for dem in DemandeEquipement.objects.all():
                data['demandes'][dem.id] = {
                    'statut': dem.statut,
                    'designation': dem.designation,
                    'demandeur': dem.demandeur.username if dem.demandeur else None
                }
            
            # Utilisateurs
            for user in CustomUser.objects.all():
                data['utilisateurs'][user.username] = {
                    'email': user.email,
                    'role': getattr(user, 'role', 'employe')
                }
            
            return data
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement des données: {e}")
            return {}
    
    def test_question_complementaire(self, question: str, expected_response: Dict[str, Any]) -> Dict[str, Any]:
        """Teste une question complémentaire et valide la réponse"""
        print(f"\n🔍 Test: {question[:60]}...")
        
        start_time = time.time()
        
        try:
            # Traitement de la question
            response = self.chatbot.process_query(question)
            
            # Extraction de la réponse textuelle
            if isinstance(response, dict):
                response_text = response.get('response', '')
                intent = response.get('intent', 'unknown')
                confidence = response.get('confidence', 0)
                source = response.get('source', 'unknown')
            else:
                response_text = str(response)
                intent = 'unknown'
                confidence = 0
                source = 'unknown'
            
            response_time = time.time() - start_time
            
            # Validation de la réponse
            validation_result = self._validate_response(
                question, response_text, expected_response, response_time
            )
            
            # Analyse du ton
            tone_analysis = self._analyze_tone(response_text)
            
            # Résultat du test
            test_result = {
                'question': question,
                'response': response_text,
                'intent': intent,
                'confidence': confidence,
                'source': source,
                'response_time': response_time,
                'validation': validation_result,
                'tone_analysis': tone_analysis,
                'timestamp': datetime.now().isoformat()
            }
            
            self.test_results.append(test_result)
            
            # Affichage du résultat
            self._display_test_result(test_result)
            
            return test_result
            
        except Exception as e:
            error_result = {
                'question': question,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            self.test_results.append(error_result)
            print(f"❌ Erreur lors du test: {e}")
            return error_result
    
    def _validate_response(self, question: str, response: str, expected: Dict[str, Any], response_time: float) -> Dict[str, Any]:
        """Valide la réponse selon les critères attendus"""
        validation = {
            'precision': 0.0,
            'completeness': 0.0,
            'performance': 0.0,
            'overall_score': 0.0,
            'details': []
        }
        
        # Validation de la performance
        if response_time < 2.0:
            validation['performance'] = 1.0
            validation['details'].append("✅ Performance: <2s")
        else:
            validation['performance'] = max(0, 1 - (response_time - 2) / 3)
            validation['details'].append(f"⚠️ Performance: {response_time:.2f}s (>2s)")
        
        # Validation de la précision
        precision_score = self._validate_precision(question, response, expected)
        validation['precision'] = precision_score
        
        # Validation de la complétude
        completeness_score = self._validate_completeness(question, response, expected)
        validation['completeness'] = completeness_score
        
        # Score global
        validation['overall_score'] = (
            validation['precision'] * 0.5 +
            validation['completeness'] * 0.3 +
            validation['performance'] * 0.2
        )
        
        return validation
    
    def _validate_precision(self, question: str, response: str, expected: Dict[str, Any]) -> float:
        """Valide la précision des informations dans la réponse"""
        score = 0.0
        details = []
        
        # Vérification des entités clés
        if 'materiels' in expected:
            for mat_code in expected['materiels']:
                if mat_code in response:
                    score += 0.2
                    details.append(f"✅ Matériel {mat_code} trouvé")
                else:
                    details.append(f"❌ Matériel {mat_code} manquant")
        
        if 'fournisseurs' in expected:
            for four_name in expected['fournisseurs']:
                if four_name in response:
                    score += 0.2
                    details.append(f"✅ Fournisseur {four_name} trouvé")
                else:
                    details.append(f"❌ Fournisseur {four_name} manquant")
        
        if 'montants' in expected:
            for montant in expected['montants']:
                if str(montant) in response:
                    score += 0.2
                    details.append(f"✅ Montant {montant} trouvé")
                else:
                    details.append(f"❌ Montant {montant} manquant")
        
        # Vérification des relations
        if 'relations' in expected:
            for relation in expected['relations']:
                if relation in response:
                    score += 0.1
                    details.append(f"✅ Relation {relation} trouvée")
                else:
                    details.append(f"❌ Relation {relation} manquante")
        
        return min(score, 1.0)
    
    def _validate_completeness(self, question: str, response: str, expected: Dict[str, Any]) -> float:
        """Valide la complétude de la réponse"""
        score = 0.0
        details = []
        
        # Vérification de la structure
        if 'Salut' in response or 'Bonjour' in response:
            score += 0.2
            details.append("✅ Introduction engageante")
        else:
            details.append("❌ Introduction manquante")
        
        if '?' in response or 'Besoin' in response or 'Veux-tu' in response:
            score += 0.2
            details.append("✅ Invitation à poursuivre")
        else:
            details.append("❌ Invitation manquante")
        
        # Vérification des détails
        if len(response.split()) > 20:
            score += 0.2
            details.append("✅ Réponse détaillée")
        else:
            details.append("❌ Réponse trop courte")
        
        # Vérification du format
        if '•' in response or '-' in response or '|' in response:
            score += 0.2
            details.append("✅ Format structuré")
        else:
            details.append("❌ Format non structuré")
        
        # Vérification de la clarté
        if 'numéro de série' in response and 'numéro de numéro de série' not in response:
            score += 0.2
            details.append("✅ Pas de répétition")
        else:
            details.append("❌ Répétition détectée")
        
        return min(score, 1.0)
    
    def _analyze_tone(self, response: str) -> Dict[str, Any]:
        """Analyse le ton de la réponse"""
        tone_analysis = {
            'human_like': 0.0,
            'professional': 0.0,
            'friendly': 0.0,
            'technical': 0.0,
            'issues': []
        }
        
        # Analyse du ton humain
        friendly_indicators = ['Salut', 'Bonjour', 'Super', 'Parfait', 'Veux-tu', 'Besoin']
        professional_indicators = ['Veuillez', 'Malheureusement', 'Désolé']
        technical_indicators = ['SQL', 'requête', 'base de données', 'jointure']
        
        friendly_count = sum(1 for indicator in friendly_indicators if indicator in response)
        professional_count = sum(1 for indicator in professional_indicators if indicator in response)
        technical_count = sum(1 for indicator in technical_indicators if indicator in response)
        
        # Calcul des scores
        total_indicators = len(friendly_indicators) + len(professional_indicators) + len(technical_indicators)
        
        if friendly_count > 0:
            tone_analysis['friendly'] = min(1.0, friendly_count / 3)
            tone_analysis['human_like'] += 0.4
        
        if professional_count > 0:
            tone_analysis['professional'] = min(1.0, professional_count / 3)
            tone_analysis['human_like'] += 0.3
        
        if technical_count > 0:
            tone_analysis['technical'] = min(1.0, technical_count / 3)
            tone_analysis['human_like'] += 0.2
        
        # Détection des problèmes
        if 'numéro de numéro de série' in response:
            tone_analysis['issues'].append("Répétition détectée")
        
        if response.count('Super') > 2 or response.count('Parfait') > 2:
            tone_analysis['issues'].append("Ton répétitif")
        
        if len(response.split('.')) > 5:
            tone_analysis['issues'].append("Réponse trop verbeuse")
        
        return tone_analysis
    
    def _display_test_result(self, result: Dict[str, Any]):
        """Affiche le résultat d'un test"""
        if 'error' in result:
            print(f"❌ ERREUR: {result['error']}")
            return
        
        validation = result['validation']
        tone = result['tone_analysis']
        
        print(f"📝 Réponse: {result['response'][:100]}...")
        print(f"🎯 Intent: {result['intent']} (confiance: {result['confidence']:.1f})")
        print(f"⚡ Source: {result['source']} - Temps: {result['response_time']:.2f}s")
        print(f"📊 Score global: {validation['overall_score']:.2f}/1.0")
        print(f"   • Précision: {validation['precision']:.2f}/1.0")
        print(f"   • Complétude: {validation['completeness']:.2f}/1.0")
        print(f"   • Performance: {validation['performance']:.2f}/1.0")
        
        if tone['issues']:
            print(f"⚠️ Problèmes de ton: {', '.join(tone['issues'])}")
        
        for detail in validation['details'][:3]:  # Afficher les 3 premiers détails
            print(f"   {detail}")
    
    def run_all_tests(self):
        """Exécute tous les tests des questions complémentaires"""
        print("\n" + "="*80)
        print("🧪 EXÉCUTION DES TESTS DES QUESTIONS COMPLÉMENTAIRES")
        print("="*80)
        
        # Questions complémentaires avec réponses attendues
        test_cases = [
            {
                'question': "Quels matériels sont stockés à l'étage 1 ?",
                'expected': {
                    'materiels': ['cd12', 'cd13', 'cd14', 'ADD/INFO/010', 'ADD/INFO/01000'],
                    'relations': ['étage 1', 'stockage']
                }
            },
            {
                'question': "Quelles demandes sont associées à la comande BC23 ?",
                'expected': {
                    'materiels': ['cd14'],
                    'relations': ['BC23', 'demande n°11']
                }
            },
            {
                'question': "Quel est le statut des livraisons pour le fourniseur 3STD ?",
                'expected': {
                    'fournisseurs': ['3STD'],
                    'relations': ['commande 123', 'retard']
                }
            },
            {
                'question': "Quels matériels informatiques sont marqués comme nouveaux ?",
                'expected': {
                    'materiels': ['ADD/INFO/010', 'ADD/INFO/01000'],
                    'relations': ['nouveaux', 'informatiques']
                }
            },
            {
                'question': "Quel est le total des comandes passées en juillet 2025 ?",
                'expected': {
                    'montants': ['6333', '3333', '2500', '500'],
                    'relations': ['juillet 2025']
                }
            },
            {
                'question': "Quels matériels sont liés à des demandes non approuvées ?",
                'expected': {
                    'relations': ['demandes non approuvées']
                }
            },
            {
                'question': "Quel fourniseur a livré le matériel ADD/INFO/01094 ?",
                'expected': {
                    'fournisseurs': ['AEBDM'],
                    'materiels': ['ADD/INFO/01094']
                }
            },
            {
                'question': "Quels matériels sont publics à l'étage 1 ?",
                'expected': {
                    'materiels': ['cd12', 'cd13', 'cd14', 'ADD/INFO/010', 'ADD/INFO/01000'],
                    'relations': ['publics', 'étage 1']
                }
            },
            {
                'question': "Combien de matériels sont en stock actuellement ?",
                'expected': {
                    'materiels': ['ADD/INFO/010', 'ADD/INFO/01000'],
                    'relations': ['en stock']
                }
            },
            {
                'question': "Quel matériel est associé au fourniseur INCONNU ?",
                'expected': {
                    'relations': ['fournisseur inexistant']
                }
            }
        ]
        
        # Exécution des tests
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{'='*60}")
            print(f"🧪 TEST {i}/10: {test_case['question']}")
            print(f"{'='*60}")
            
            self.test_question_complementaire(
                test_case['question'], 
                test_case['expected']
            )
            
            # Pause entre les tests
            time.sleep(1)
        
        # Génération du rapport final
        self._generate_final_report()
    
    def _generate_final_report(self):
        """Génère le rapport final des tests"""
        print("\n" + "="*80)
        print("📊 RAPPORT FINAL DES TESTS")
        print("="*80)
        
        if not self.test_results:
            print("❌ Aucun résultat de test disponible")
            return
        
        # Statistiques globales
        successful_tests = [r for r in self.test_results if 'error' not in r]
        failed_tests = [r for r in self.test_results if 'error' in r]
        
        if successful_tests:
            avg_precision = sum(r['validation']['precision'] for r in successful_tests) / len(successful_tests)
            avg_completeness = sum(r['validation']['completeness'] for r in successful_tests) / len(successful_tests)
            avg_performance = sum(r['validation']['performance'] for r in successful_tests) / len(successful_tests)
            avg_overall = sum(r['validation']['overall_score'] for r in successful_tests) / len(successful_tests)
            avg_response_time = sum(r['response_time'] for r in successful_tests) / len(successful_tests)
            
            print(f"✅ Tests réussis: {len(successful_tests)}/10")
            print(f"❌ Tests échoués: {len(failed_tests)}/10")
            print(f"📊 Scores moyens:")
            print(f"   • Précision: {avg_precision:.2f}/1.0")
            print(f"   • Complétude: {avg_completeness:.2f}/1.0")
            print(f"   • Performance: {avg_performance:.2f}/1.0")
            print(f"   • Global: {avg_overall:.2f}/1.0")
            print(f"⚡ Temps de réponse moyen: {avg_response_time:.2f}s")
            
            # Analyse des problèmes
            all_issues = []
            for result in successful_tests:
                if result['tone_analysis']['issues']:
                    all_issues.extend(result['tone_analysis']['issues'])
            
            if all_issues:
                print(f"\n⚠️ Problèmes détectés:")
                issue_counts = {}
                for issue in all_issues:
                    issue_counts[issue] = issue_counts.get(issue, 0) + 1
                
                for issue, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True):
                    print(f"   • {issue}: {count} occurrence(s)")
            
            # Recommandations
            print(f"\n💡 Recommandations:")
            if avg_precision < 0.8:
                print("   • Améliorer la précision des réponses (données incorrectes)")
            if avg_completeness < 0.7:
                print("   • Améliorer la complétude (détails manquants)")
            if avg_performance < 0.9:
                print("   • Optimiser les performances (temps de réponse)")
            if avg_overall >= 0.8:
                print("   • Excellent! Le chatbot répond aux exigences")
            elif avg_overall >= 0.6:
                print("   • Bon niveau, quelques améliorations nécessaires")
            else:
                print("   • Améliorations importantes nécessaires")
        
        # Sauvegarde des résultats
        self._save_test_results()
        
        total_time = time.time() - self.start_time
        print(f"\n⏱️ Temps total d'exécution: {total_time:.2f}s")
    
    def _save_test_results(self):
        """Sauvegarde les résultats des tests"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_results_complementaires_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.test_results, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"💾 Résultats sauvegardés dans: {filename}")
            
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")


def main():
    """Fonction principale"""
    print("🚀 Testeur de Chatbot ParcInfo - Questions Complémentaires v2.0")
    print("📅 Date: 18/08/2025")
    print("🎯 Objectif: Valider les améliorations du chatbot")
    
    try:
        # Initialisation du testeur
        tester = ChatbotTesterV2()
        
        # Exécution des tests
        tester.run_all_tests()
        
        print("\n✅ Tests terminés avec succès!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrompus par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
