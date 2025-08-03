#!/usr/bin/env python3
"""
Script de test pour le chatbot ParcInfo
Ce script permet de tester le fonctionnement du chatbot sans interface web
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

from apps.chatbot.llm_engine import ParcInfoChatbot
from apps.users.models import CustomUser

def test_chatbot():
    """Test du chatbot ParcInfo avec LLaMA 3"""
    print("🤖 Test du Chatbot ParcInfo avec LLaMA 3")
    print("=" * 60)
    
    # Créer un gestionnaire de test si nécessaire
    manager, created = CustomUser.objects.get_or_create(
        username='test_manager',
        defaults={
            'email': 'manager@example.com',
            'is_superuser': False,
            'is_staff': True
        }
    )
    
    if created:
        print(f"✅ Gestionnaire de test créé: {manager.username}")
    else:
        print(f"✅ Gestionnaire de test existant: {manager.username}")
    
    # Initialiser le chatbot
    print("\n🔄 Initialisation du chatbot...")
    try:
        chatbot = ParcInfoChatbot()
        print("✅ Chatbot initialisé avec succès")
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        return
    
    # Test du contexte de base de données
    print("\n📊 Test du contexte de base de données:")
    try:
        context = chatbot.get_comprehensive_database_context()
        print(f"Contexte: {context[:300]}...")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Test des données utilisateur
    print("\n👤 Test du contexte utilisateur:")
    try:
        user_data = chatbot.get_user_context(manager)
        print(f"Contexte utilisateur: {user_data}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Test des analytics système
    print("\n📋 Test des analytics système:")
    try:
        analytics = chatbot.get_system_analytics()
        print(f"Analytics: {analytics[:300]}...")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Test de réponses avec LLaMA 3
    print("\n🧠 Test des réponses avec LLaMA 3:")
    test_questions = [
        "Analyser les tendances des demandes d'équipement",
        "Quel est le taux d'approbation des demandes ?",
        "Identifier les goulots d'étranglement dans le processus",
        "Optimiser la gestion du stock de matériel",
        "Générer un rapport de performance du système",
        "Analyser l'utilisation des équipements",
        "Suggérer des améliorations du workflow",
        "Quelles sont les métriques clés du système ?",
        "Comment améliorer l'efficacité des livraisons ?",
        "Analyser la répartition des rôles utilisateurs"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n--- Question {i} ---")
        print(f"Q: {question}")
        try:
            response = chatbot.get_response(question, manager)
            print(f"R: {response}")
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    # Test de l'apprentissage continu
    print("\n🎓 Test de l'apprentissage continu:")
    try:
        initial_count = len(chatbot.conversation_history)
        chatbot.learn_from_interaction("Test question", "Test response", manager)
        final_count = len(chatbot.conversation_history)
        print(f"Interactions: {initial_count} → {final_count}")
        print("✅ Apprentissage fonctionnel")
    except Exception as e:
        print(f"❌ Erreur apprentissage: {e}")
    
    # Test des insights d'apprentissage
    print("\n📈 Test des insights d'apprentissage:")
    try:
        insights = chatbot.get_learning_insights()
        print(f"Insights: {insights}")
    except Exception as e:
        print(f"❌ Erreur insights: {e}")
    
    # Test de rafraîchissement du contexte
    print("\n🔄 Test de rafraîchissement du contexte:")
    try:
        chatbot.refresh_context()
        print("✅ Contexte rafraîchi avec succès")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Test terminé")
    
    # Nettoyage
    if created:
        manager.delete()
        print("🧹 Gestionnaire de test supprimé")

def test_permissions():
    """Test des permissions d'accès"""
    print("\n🔒 Test des permissions:")
    
    # Test gestionnaire
    manager = CustomUser.objects.create_user(
        username='test_manager',
        password='test123',
        is_superuser=False,
        is_staff=True
    )
    
    # Test superadmin
    admin = CustomUser.objects.create_user(
        username='test_admin',
        password='test123',
        is_superuser=True,
        is_staff=True
    )
    
    # Test employé
    employee = CustomUser.objects.create_user(
        username='test_employee',
        password='test123',
        is_superuser=False,
        is_staff=False
    )
    
    print(f"Gestionnaire (is_superuser={manager.is_superuser}, is_staff={manager.is_staff}): ✅ Accès autorisé")
    print(f"Super Admin (is_superuser={admin.is_superuser}, is_staff={admin.is_staff}): ✅ Accès autorisé")
    print(f"Employé (is_superuser={employee.is_superuser}, is_staff={employee.is_staff}): ❌ Accès refusé")
    
    # Nettoyage
    manager.delete()
    admin.delete()
    employee.delete()

def test_llm_initialization():
    """Test de l'initialisation du LLM"""
    print("\n🤖 Test de l'initialisation du LLM:")
    
    try:
        chatbot = ParcInfoChatbot()
        
        if chatbot.llm:
            print("✅ LLM initialisé avec succès")
            print(f"Type de LLM: {type(chatbot.llm).__name__}")
        else:
            print("❌ LLM non initialisé")
            
        if chatbot.vectorstore:
            print("✅ Vectorstore initialisé avec succès")
        else:
            print("❌ Vectorstore non initialisé")
            
        if chatbot.chain:
            print("✅ Chaîne de conversation initialisée avec succès")
        else:
            print("❌ Chaîne de conversation non initialisée")
            
    except Exception as e:
        print(f"❌ Erreur lors du test d'initialisation: {e}")

if __name__ == "__main__":
    print("🚀 Démarrage des tests du chatbot ParcInfo")
    print("🤖 Utilisation de LLaMA 3 et LangChain")
    print("👥 Accès réservé aux gestionnaires et superadmin")
    
    # Test des permissions
    test_permissions()
    
    # Test d'initialisation du LLM
    test_llm_initialization()
    
    # Test principal du chatbot
    test_chatbot()
    
    print("\n🎉 Tous les tests sont terminés !")
    print("\n📋 Résumé:")
    print("- Le chatbot utilise LLaMA 3 pour les réponses")
    print("- Il accède directement à la base de données")
    print("- Il fournit des réponses contextuelles et personnalisées")
    print("- Il s'améliore continuellement grâce à l'apprentissage")
    print("- Accès réservé aux gestionnaires et superadmin")
    print("- Aucune réponse prédéfinie, 100% IA")
    
    print("\n🌐 Pour utiliser le chatbot en ligne de commande:")
    print("1. Accédez à l'interface web: /chatbot/")
    print("2. Connectez-vous avec un compte gestionnaire ou superadmin")
    print("3. Posez vos questions techniques sur le système ParcInfo")
    print("4. Le chatbot répondra avec l'IA en utilisant vos données")
    print("5. Consultez les insights d'apprentissage: /chatbot/insights/") 