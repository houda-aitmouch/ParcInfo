#!/usr/bin/env python3
"""
Test script for the improved ParcInfo Chatbot
Tests the corrected functionality and improved precision
"""

import os
import sys
import django
import json
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

from apps.chatbot.core_chatbot_improved import ParcInfoChatbotImproved

def test_improved_chatbot():
    """Test the improved chatbot with specific problematic queries"""
    
    print("🚀 Testing Improved ParcInfo Chatbot...")
    print("=" * 60)
    
    # Initialize the improved chatbot
    try:
        chatbot = ParcInfoChatbotImproved()
        print("✅ Chatbot initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize chatbot: {e}")
        return
    
    # Test cases that were problematic in the original version
    test_cases = [
        {
            "category": "🟢 Questions Faciles (Corrigées)",
            "questions": [
                "Qui est le super admin ?",
                "Liste des fournisseurs",
                "Donne-moi les commandes récentes",
                "Montre-moi la liste du matériel en service",
                "Quels sont les utilisateurs du système ?",
                "Livraisons à venir",
                "Code inventaire de la baie"
            ]
        },
        {
            "category": "🟡 Questions Intermédiaires (Corrigées)",
            "questions": [
                "Quels sont les équipements non affectés ?",
                "Quels utilisateurs n'ont encore rien reçu comme matériel ?",
                "Qui utilise le matériel avec le code inventaire cd12 ?",
                "Donne-moi les équipements du type 'PC' stockés à l'étage 1",
                "Quels fournisseurs ont livré plus de 3 équipements ?",
                "Quel est le nom du fournisseur qui a livré l'équipement eq18 ?",
                "Commandes livrées mais avec un équipement non encore affecté"
            ]
        },
        {
            "category": "🔴 Questions Complexes (Corrigées)",
            "questions": [
                "Quel est le fournisseur ayant livré le plus de matériel au total ?",
                "Taux de livraison des commandes contenant du matériel informatique",
                "Combien d'équipements en bon état, non affectés, sont actuellement en stock ?",
                "Pourcentage des équipements affectés qui ont été commandés en 2023",
                "Historique complet de l'équipement EQ18 : commande, livraison, affectation",
                "Fournisseurs ayant livré à la fois du matériel informatique et bureautique",
                "Résumé par type (PC, serveur, imprimante) avec nombre total, livrés et affectés"
            ]
        }
    ]
    
    results = {}
    
    for test_category in test_cases:
        category = test_category["category"]
        questions = test_category["questions"]
        
        print(f"\n{category}")
        print("-" * 50)
        
        results[category] = []
        
        for i, question in enumerate(questions, 1):
            print(f"\n{i}. Question: {question}")
            
            try:
                start_time = datetime.now()
                
                # Process the query
                response = chatbot.process_query(question)
                
                end_time = datetime.now()
                processing_time = (end_time - start_time).total_seconds()
                
                # Extract response text
                if isinstance(response, dict):
                    response_text = response.get('response', str(response))
                    confidence = response.get('confidence', 0)
                    method = response.get('method', 'unknown')
                else:
                    response_text = str(response)
                    confidence = 0
                    method = 'unknown'
                
                # Analyze response quality
                quality_score = analyze_response_quality(question, response_text)
                
                print(f"   ⏱️  Temps: {processing_time:.3f}s")
                print(f"   🎯 Confiance: {confidence}")
                print(f"   🔧 Méthode: {method}")
                print(f"   📊 Qualité: {quality_score}/100")
                print(f"   💬 Réponse: {response_text[:200]}{'...' if len(response_text) > 200 else ''}")
                
                # Store results
                results[category].append({
                    "question": question,
                    "response": response_text,
                    "processing_time": processing_time,
                    "confidence": confidence,
                    "method": method,
                    "quality_score": quality_score,
                    "success": quality_score >= 70
                })
                
            except Exception as e:
                print(f"   ❌ Erreur: {e}")
                results[category].append({
                    "question": question,
                    "error": str(e),
                    "success": False
                })
    
    # Generate summary report
    generate_summary_report(results)
    
    # Save detailed results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"improved_chatbot_test_{timestamp}.json"
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n📁 Résultats détaillés sauvegardés dans: {results_file}")

def analyze_response_quality(question: str, response: str) -> int:
    """Analyze the quality of a chatbot response"""
    if not response or len(response.strip()) < 10:
        return 0
    
    score = 0
    
    # Length score (0-20 points)
    if len(response) > 100:
        score += 20
    elif len(response) > 50:
        score += 15
    elif len(response) > 20:
        score += 10
    else:
        score += 5
    
    # Relevance score (0-30 points)
    question_lower = question.lower()
    response_lower = response.lower()
    
    # Check if response contains relevant keywords
    relevant_words = extract_relevant_words(question_lower)
    found_words = sum(1 for word in relevant_words if word in response_lower)
    
    if found_words > 0:
        score += min(30, (found_words / len(relevant_words)) * 30)
    
    # Structure score (0-25 points)
    if any(marker in response for marker in ['•', '-', '*', '1.', '2.']):
        score += 15  # Has bullet points
    if any(marker in response for marker in ['**', '__', '==']):
        score += 10  # Has formatting
    
    # Completeness score (0-25 points)
    if 'aucun' not in response_lower or 'trouvé' not in response_lower:
        score += 15  # Not a "no results" response
    if len(response.split('\n')) > 3:
        score += 10  # Multiple lines of content
    
    return min(100, int(score))

def extract_relevant_words(question: str) -> list:
    """Extract relevant words from a question for relevance checking"""
    # Remove common words
    stop_words = {
        'qui', 'est', 'les', 'des', 'du', 'de', 'la', 'le', 'et', 'ou', 'avec',
        'pour', 'dans', 'sur', 'par', 'vers', 'chez', 'que', 'quel', 'quelle',
        'quels', 'quelles', 'sont', 'ont', 'a', 'à', 'un', 'une', 'au', 'aux'
    }
    
    words = question.split()
    relevant = [word for word in words if len(word) > 2 and word not in stop_words]
    
    return relevant

def generate_summary_report(results: dict):
    """Generate a summary report of the test results"""
    print("\n" + "=" * 60)
    print("📊 RAPPORT DE TEST - CHATBOT AMÉLIORÉ")
    print("=" * 60)
    
    total_questions = 0
    total_successful = 0
    total_processing_time = 0
    total_quality_score = 0
    
    for category, questions in results.items():
        print(f"\n{category}")
        print("-" * 40)
        
        category_questions = len(questions)
        category_successful = sum(1 for q in questions if q.get('success', False))
        category_avg_time = sum(q.get('processing_time', 0) for q in questions) / category_questions if category_questions > 0 else 0
        category_avg_quality = sum(q.get('quality_score', 0) for q in questions) / category_questions if category_questions > 0 else 0
        
        print(f"Questions: {category_questions}")
        print(f"Réussites: {category_successful}/{category_questions} ({category_successful/category_questions*100:.1f}%)")
        print(f"Temps moyen: {category_avg_time:.3f}s")
        print(f"Qualité moyenne: {category_avg_quality:.1f}/100")
        
        total_questions += category_questions
        total_successful += category_successful
        total_processing_time += sum(q.get('processing_time', 0) for q in questions)
        total_quality_score += sum(q.get('quality_score', 0) for q in questions)
    
    print("\n" + "=" * 60)
    print("📈 RÉSULTATS GLOBAUX")
    print("=" * 60)
    print(f"Total des questions: {total_questions}")
    print(f"Total des réussites: {total_successful}/{total_questions} ({total_successful/total_questions*100:.1f}%)")
    print(f"Temps de traitement moyen: {total_processing_time/total_questions:.3f}s")
    print(f"Qualité moyenne globale: {total_quality_score/total_questions:.1f}/100")
    
    # Improvement assessment
    if total_successful/total_questions >= 0.8:
        print("\n🎉 EXCELLENT! Le chatbot amélioré fonctionne très bien!")
    elif total_successful/total_questions >= 0.6:
        print("\n✅ BON! Le chatbot amélioré montre une amélioration significative!")
    elif total_successful/total_questions >= 0.4:
        print("\n⚠️ MOYEN! Le chatbot amélioré montre quelques améliorations.")
    else:
        print("\n❌ INSUFFISANT! Le chatbot amélioré nécessite plus de corrections.")

if __name__ == "__main__":
    test_improved_chatbot()
