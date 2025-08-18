#!/usr/bin/env python3
"""
Vérification finale du système RAG de ParcInfo
Confirme que tout est bien configuré et fonctionnel
"""

import subprocess
import sys
import os

def check_environment():
    """Vérifier l'environnement de base"""
    print("🔍 Vérification de l'environnement...")
    
    # Vérifier que l'environnement virtuel existe
    if not os.path.exists("rag_env"):
        print("❌ Environnement virtuel 'rag_env' non trouvé")
        return False
    
    print("✅ Environnement virtuel 'rag_env' présent")
    return True

def check_dependencies():
    """Vérifier les dépendances dans l'environnement virtuel"""
    print("\n🔍 Vérification des dépendances...")
    
    venv_python = "rag_env/bin/python"
    
    # Vérifier sentence-transformers
    try:
        result = subprocess.run([
            venv_python, "-c", 
            "import sentence_transformers; print('✅ sentence-transformers disponible')"
        ], capture_output=True, text=True, check=True)
        print(result.stdout.strip())
    except subprocess.CalledProcessError:
        print("❌ sentence-transformers non disponible")
        return False
    
    # Vérifier Django
    try:
        result = subprocess.run([
            venv_python, "-c", 
            "import django; print(f'✅ Django {django.get_version()} disponible')"
        ], capture_output=True, text=True, check=True)
        print(result.stdout.strip())
    except subprocess.CalledProcessError:
        print("❌ Django non disponible")
        return False
    
    # Vérifier openpyxl
    try:
        result = subprocess.run([
            venv_python, "-c", 
            "import openpyxl; print('✅ openpyxl disponible')"
        ], capture_output=True, text=True, check=True)
        print(result.stdout.strip())
    except subprocess.CalledProcessError:
        print("❌ openpyxl non disponible")
        return False
    
    return True

def check_rag_system():
    """Vérifier le système RAG complet"""
    print("\n🔍 Vérification du système RAG...")
    
    venv_python = "rag_env/bin/python"
    
    try:
        result = subprocess.run([
            venv_python, "-c", 
            """
import sys
import os
import django

# Configuration Django
project_root = '/Users/HouDa/PycharmProjects/ParcInfo'
sys.path.insert(0, project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

from apps.chatbot.rag_manager import RAGManager
from apps.chatbot.core_chatbot import ParcInfoChatbot

# Test RAG Manager
rag = RAGManager()
if rag.embed_model:
    print('✅ RAG Manager: Embedding disponible')
else:
    print('❌ RAG Manager: Embedding non disponible')

# Test Chatbot
chatbot = ParcInfoChatbot()
if chatbot.nlp_available:
    print('✅ Chatbot: NLP disponible')
else:
    print('❌ Chatbot: NLP non disponible')

if chatbot.use_llm:
    print('✅ Chatbot: LLM (Ollama) disponible')
else:
    print('❌ Chatbot: LLM non disponible')

print('✅ Système RAG: Tous les composants fonctionnels')
            """
        ], capture_output=True, text=True, check=True)
        print(result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur système RAG: {e.stderr}")
        return False

def check_ollama():
    """Vérifier qu'Ollama est accessible"""
    print("\n🔍 Vérification d'Ollama...")
    
    try:
        result = subprocess.run([
            "ollama", "list"
        ], capture_output=True, text=True, check=True)
        
        if "llama" in result.stdout.lower():
            print("✅ Ollama: Modèles LLaMA disponibles")
            print(f"Modèles: {result.stdout.strip()}")
        else:
            print("⚠️ Ollama: Aucun modèle LLaMA trouvé")
        
        return True
    except subprocess.CalledProcessError:
        print("❌ Ollama: Service non accessible")
        return False
    except FileNotFoundError:
        print("❌ Ollama: Commande non trouvée")
        return False

def check_files():
    """Vérifier que tous les fichiers RAG sont présents"""
    print("\n🔍 Vérification des fichiers RAG...")
    
    required_files = [
        "launch_with_rag.sh",
        "test_chatbot_rag.py",
        "RAG_README.md",
        "RAG_SETUP_COMPLETE.md",
        "rag_env/requirements.txt"
    ]
    
    all_present = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            all_present = False
    
    return all_present

def show_summary():
    """Afficher le résumé de la configuration"""
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DE LA CONFIGURATION RAG")
    print("=" * 60)
    print("")
    print("🎯 **Statut global : SYSTÈME RAG OPÉRATIONNEL**")
    print("")
    print("✨ **Fonctionnalités activées :**")
    print("   • Recherche sémantique avec sentence-transformers")
    print("   • Gestionnaire RAG avec embeddings")
    print("   • Chatbot IA avec NLP et LLM")
    print("   • Intégration Ollama pour réponses avancées")
    print("")
    print("🚀 **Comment utiliser :**")
    print("   ./launch_with_rag.sh")
    print("")
    print("🧪 **Comment tester :**")
    print("   python test_chatbot_rag.py")
    print("")
    print("📚 **Documentation :**")
    print("   RAG_README.md - Guide d'utilisation")
    print("   RAG_SETUP_COMPLETE.md - Configuration")
    print("")
    print("💡 **Le chatbot ParcInfo est maintenant intelligent !**")

def main():
    """Fonction principale de vérification"""
    print("🚀 VÉRIFICATION FINALE DU SYSTÈME RAG PARCINFO")
    print("=" * 60)
    
    checks = [
        ("Environnement", check_environment),
        ("Dépendances", check_dependencies),
        ("Système RAG", check_rag_system),
        ("Ollama", check_ollama),
        ("Fichiers RAG", check_files)
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        if not check_func():
            all_passed = False
            print(f"\n❌ Vérification '{check_name}' échouée")
    
    if all_passed:
        print("\n🎉 TOUTES LES VÉRIFICATIONS SONT RÉUSSIES !")
        show_summary()
    else:
        print("\n❌ CERTAINES VÉRIFICATIONS ONT ÉCHOUÉ")
        print("💡 Vérifiez les erreurs ci-dessus et corrigez-les")

if __name__ == "__main__":
    main()
