#!/usr/bin/env python3
"""
Script d'analyse des performances du chatbot ParcInfo
Analyse les résultats des tests progressifs et génère un rapport détaillé
"""

import json
import os
from datetime import datetime

def analyze_chatbot_performance(test_file):
    """Analyse les performances du chatbot à partir du fichier de test"""
    
    print("🔍 ANALYSE DES PERFORMANCES DU CHATBOT PARCINFO")
    print("=" * 80)
    
    # Charger les résultats
    with open(test_file, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    # Statistiques globales
    total_questions = 0
    total_successful = 0
    total_processing_time = 0
    confidence_scores = []
    
    # Analyse par catégorie
    category_analysis = {}
    
    for category, questions in results["categories"].items():
        category_total = len(questions)
        category_success = sum(1 for q in questions if q["status"] == "success")
        category_processing_time = sum(q["processing_time"] for q in questions if q["status"] == "success")
        category_confidence = [q["confidence"] for q in questions if q["status"] == "success"]
        
        # Méthodes utilisées
        methods = {}
        sources = {}
        intents = {}
        
        for q in questions:
            if q["status"] == "success":
                method = q["method"]
                source = q["source"]
                intent = q["intent"]
                
                methods[method] = methods.get(method, 0) + 1
                sources[source] = sources.get(source, 0) + 1
                intents[intent] = intents.get(intent, 0) + 1
        
        category_analysis[category] = {
            "total": category_total,
            "success": category_success,
            "success_rate": (category_success / category_total) * 100,
            "avg_processing_time": category_processing_time / category_success if category_success > 0 else 0,
            "avg_confidence": sum(category_confidence) / len(category_confidence) if category_confidence else 0,
            "methods": methods,
            "sources": sources,
            "intents": intents
        }
        
        total_questions += category_total
        total_successful += category_success
        total_processing_time += category_processing_time
        confidence_scores.extend(category_confidence)
    
    # Affichage des résultats
    print(f"\n📊 RÉSULTATS GLOBAUX")
    print(f"   Total des questions : {total_questions}")
    print(f"   Questions réussies : {total_successful}")
    print(f"   Taux de réussite global : {(total_successful/total_questions)*100:.1f}%")
    print(f"   Temps de traitement moyen : {total_processing_time/total_successful:.3f}s")
    print(f"   Confiance moyenne : {sum(confidence_scores)/len(confidence_scores):.1f}")
    
    # Analyse par catégorie
    print(f"\n📋 ANALYSE PAR CATÉGORIE")
    print("=" * 80)
    
    for category, analysis in category_analysis.items():
        print(f"\n{category}")
        print(f"   Questions : {analysis['total']}")
        print(f"   Taux de réussite : {analysis['success_rate']:.1f}%")
        print(f"   Temps moyen : {analysis['avg_processing_time']:.3f}s")
        print(f"   Confiance moyenne : {analysis['avg_confidence']:.1f}")
        
        print(f"   Méthodes utilisées :")
        for method, count in analysis['methods'].items():
            percentage = (count / analysis['success']) * 100
            print(f"     • {method}: {count} ({percentage:.1f}%)")
        
        print(f"   Sources de données :")
        for source, count in analysis['sources'].items():
            percentage = (count / analysis['success']) * 100
            print(f"     • {source}: {count} ({percentage:.1f}%)")
    
    # Analyse des performances
    print(f"\n🚀 ANALYSE DES PERFORMANCES")
    print("=" * 80)
    
    # Questions les plus rapides
    all_questions = []
    for category, questions in results["categories"].items():
        for q in questions:
            if q["status"] == "success":
                all_questions.append({
                    "question": q["question"],
                    "processing_time": q["processing_time"],
                    "confidence": q["confidence"],
                    "method": q["method"],
                    "category": category
                })
    
    # Top 5 des questions les plus rapides
    fastest_questions = sorted(all_questions, key=lambda x: x["processing_time"])[:5]
    print(f"\n⚡ TOP 5 - Questions les plus rapides :")
    for i, q in enumerate(fastest_questions, 1):
        print(f"   {i}. {q['question'][:60]}... ({q['processing_time']:.3f}s, conf: {q['confidence']})")
    
    # Top 5 des questions les plus lentes
    slowest_questions = sorted(all_questions, key=lambda x: x["processing_time"], reverse=True)[:5]
    print(f"\n🐌 TOP 5 - Questions les plus lentes :")
    for i, q in enumerate(slowest_questions, 1):
        print(f"   {i}. {q['question'][:60]}... ({q['processing_time']:.3f}s, conf: {q['confidence']})")
    
    # Questions avec la plus haute confiance
    highest_confidence = sorted(all_questions, key=lambda x: x["confidence"], reverse=True)[:5]
    print(f"\n🎯 TOP 5 - Questions avec la plus haute confiance :")
    for i, q in enumerate(highest_confidence, 1):
        print(f"   {i}. {q['question'][:60]}... (conf: {q['confidence']}, {q['processing_time']:.3f}s)")
    
    # Questions avec la plus basse confiance
    lowest_confidence = sorted(all_questions, key=lambda x: x["confidence"])[:5]
    print(f"\n❓ TOP 5 - Questions avec la plus basse confiance :")
    for i, q in enumerate(lowest_confidence, 1):
        print(f"   {i}. {q['question'][:60]}... (conf: {q['confidence']}, {q['processing_time']:.3f}s)")
    
    # Analyse des méthodes
    print(f"\n🔧 ANALYSE DES MÉTHODES")
    print("=" * 80)
    
    method_stats = {}
    for q in all_questions:
        method = q["method"]
        if method not in method_stats:
            method_stats[method] = {"count": 0, "total_time": 0, "confidences": []}
        
        method_stats[method]["count"] += 1
        method_stats[method]["total_time"] += q["processing_time"]
        method_stats[method]["confidences"].append(q["confidence"])
    
    for method, stats in method_stats.items():
        avg_time = stats["total_time"] / stats["count"]
        avg_confidence = sum(stats["confidences"]) / len(stats["confidences"])
        print(f"\n   {method}:")
        print(f"     • Utilisée : {stats['count']} fois")
        print(f"     • Temps moyen : {avg_time:.3f}s")
        print(f"     • Confiance moyenne : {avg_confidence:.1f}")
    
    # Recommandations
    print(f"\n💡 RECOMMANDATIONS")
    print("=" * 80)
    
    if category_analysis["🟢 Facile — Questions directes (données brutes)"]["success_rate"] < 95:
        print("   • Améliorer la reconnaissance des questions simples")
    
    if category_analysis["🟡 Intermédiaire — Filtres simples & conditions"]["success_rate"] < 90:
        print("   • Optimiser la gestion des filtres et conditions")
    
    if category_analysis["🔴 Difficile — Analyse croisée & statistiques"]["success_rate"] < 85:
        print("   • Renforcer les capacités d'analyse croisée")
    
    # Identifier les méthodes lentes
    slow_methods = [method for method, stats in method_stats.items() 
                    if stats["total_time"] / stats["count"] > 1.0]
    if slow_methods:
        print(f"   • Optimiser les méthodes lentes : {', '.join(slow_methods)}")
    
    # Identifier les méthodes avec faible confiance
    low_confidence_methods = [method for method, stats in method_stats.items() 
                             if sum(stats["confidences"]) / len(stats["confidences"]) < 50]
    if low_confidence_methods:
        print(f"   • Améliorer la confiance des méthodes : {', '.join(low_confidence_methods)}")
    
    print(f"\n✅ Analyse terminée !")
    return category_analysis

if __name__ == "__main__":
    # Chercher le fichier de test le plus récent
    test_files = [f for f in os.listdir('.') if f.startswith('progressive_questions_test_') and f.endswith('.json')]
    
    if not test_files:
        print("❌ Aucun fichier de test trouvé")
        exit(1)
    
    # Prendre le plus récent
    latest_test = max(test_files)
    print(f"📁 Fichier de test utilisé : {latest_test}")
    
    # Analyser les performances
    analysis = analyze_chatbot_performance(latest_test)
