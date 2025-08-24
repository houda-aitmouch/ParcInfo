#!/usr/bin/env python
import os
import sys
import django
import json
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

from apps.chatbot.core_chatbot import ChatbotCore
from apps.users.models import CustomUser
from apps.demande_equipement.models import DemandeEquipement
from apps.materiel_informatique.models import MaterielInformatique
from apps.materiel_bureautique.models import MaterielBureau

def test_rag_chatbot():
    """Test du chatbot avec RAG activé"""
    
    print("🧪 Test du Chatbot avec RAG activé")
    print("=" * 50)
    
    # Initialiser le chatbot
    try:
        chatbot = ChatbotCore()
        print("✅ Chatbot initialisé avec succès")
    except Exception as e:
        print(f"❌ Erreur d'initialisation du chatbot: {e}")
        return False
    
    # Questions de test
    test_questions = [
        "Combien d'utilisateurs y a-t-il dans le système ?",
        "Liste les matériels informatiques",
        "Quels sont les fournisseurs disponibles ?",
        "Montre-moi les commandes récentes",
        "Y a-t-il des garanties qui expirent bientôt ?"
    ]
    
    results = []
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Question: {question}")
        
        try:
            # Traiter la requête
            response = chatbot.process_query(question, user_id='test_user')
            
            if response:
                print(f"✅ Réponse générée ({len(response.get('response', ''))} caractères)")
                print(f"📊 Intent détecté: {response.get('intent', 'N/A')}")
                print(f"🎯 Confiance: {response.get('confidence', 0):.2f}")
                
                # Afficher un extrait de la réponse
                response_text = response.get('response', '')
                if response_text:
                    preview = response_text[:200] + "..." if len(response_text) > 200 else response_text
                    print(f"💬 Réponse: {preview}")
                    
                    # Enregistrer le résultat
                    results.append({
                        'question': question,
                        'response': response_text,
                        'intent': response.get('intent', 'N/A'),
                        'confidence': response.get('confidence', 0),
                        'success': True
                    })
                else:
                    print("❌ Réponse vide")
                    results.append({
                        'question': question,
                        'error': 'Réponse vide',
                        'success': False
                    })
            else:
                print("❌ Aucune réponse générée")
                results.append({
                    'question': question,
                    'error': 'Aucune réponse générée',
                    'success': False
                })
                
        except Exception as e:
            print(f"❌ Erreur lors du traitement: {e}")
            results.append({
                'question': question,
                'error': str(e),
                'success': False
            })
    
    # Générer le rapport de test
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"test_report_{timestamp}.json"
    
    report = {
        'timestamp': timestamp,
        'total_questions': len(test_questions),
        'successful_responses': len([r for r in results if r.get('success', False)]),
        'failed_responses': len([r for r in results if not r.get('success', False)]),
        'success_rate': len([r for r in results if r.get('success', False)]) / len(test_questions) * 100,
        'results': results
    }
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 50)
    print(f"📊 Rapport de test généré: {report_file}")
    print(f"✅ Réponses réussies: {report['successful_responses']}/{report['total_questions']}")
    print(f"📈 Taux de succès: {report['success_rate']:.1f}%")
    print("🏁 Test terminé")
    
    return report['success_rate'] > 50  # Retourner True si plus de 50% de succès

if __name__ == '__main__':
    success = test_rag_chatbot()
    sys.exit(0 if success else 1)
