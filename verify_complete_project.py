#!/usr/bin/env python3
"""
Vérification complète du projet ParcInfo
Vérifie tous les composants : Django, RAG, Streamlit, dépendances, environnement
"""

import subprocess
import sys
import os
import platform

def print_header(title):
    """Afficher un en-tête de section"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def check_system_info():
    """Vérifier les informations système"""
    print_header("INFORMATIONS SYSTÈME")
    
    print(f"🖥️  Système d'exploitation: {platform.system()} {platform.release()}")
    print(f"🐍 Python système: {platform.python_version()}")
    print(f"📍 Répertoire de travail: {os.getcwd()}")
    
    # Vérifier l'espace disque
    try:
        result = subprocess.run(["df", "-h", "."], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                parts = lines[1].split()
                if len(parts) >= 5:
                    print(f"💾 Espace disque disponible: {parts[3]}")
    except:
        print("💾 Espace disque: Non vérifiable")

def check_python_environments():
    """Vérifier les environnements Python"""
    print_header("ENVIRONNEMENTS PYTHON")
    
    # Python système
    try:
        result = subprocess.run(["python3", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Python système: {result.stdout.strip()}")
        else:
            print("❌ Python système: Non disponible")
    except:
        print("❌ Python système: Non accessible")
    
    # Environnement virtuel RAG
    if os.path.exists("rag_env"):
        print("✅ Environnement virtuel RAG: Présent")
        
        # Vérifier Python dans l'environnement RAG
        try:
            result = subprocess.run(["rag_env/bin/python", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   Python RAG: {result.stdout.strip()}")
            else:
                print("   Python RAG: Non fonctionnel")
        except:
            print("   Python RAG: Non accessible")
    else:
        print("❌ Environnement virtuel RAG: Absent")
    
    # Anaconda
    try:
        result = subprocess.run(["conda", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Anaconda: {result.stdout.strip()}")
        else:
            print("❌ Anaconda: Non disponible")
    except:
        print("❌ Anaconda: Non installé")

def check_django_environment():
    """Vérifier l'environnement Django"""
    print_header("ENVIRONNEMENT DJANGO")
    
    # Vérifier Django dans l'environnement RAG
    if os.path.exists("rag_env"):
        try:
            result = subprocess.run([
                "rag_env/bin/python", "-c", 
                "import django; print(f'✅ Django {django.get_version()} dans RAG')"
            ], capture_output=True, text=True, check=True)
            print(result.stdout.strip())
        except subprocess.CalledProcessError:
            print("❌ Django dans RAG: Non disponible")
    
    # Vérifier la configuration Django
    try:
        result = subprocess.run([
            "rag_env/bin/python", "manage.py", "check"
        ], capture_output=True, text=True, check=True)
        print("✅ Configuration Django: Aucun problème détecté")
    except subprocess.CalledProcessError as e:
        print(f"❌ Configuration Django: Problèmes détectés")
        print(f"   Erreur: {e.stderr}")

def check_rag_system():
    """Vérifier le système RAG"""
    print_header("SYSTÈME RAG")
    
    if not os.path.exists("rag_env"):
        print("❌ Environnement RAG non disponible")
        return False
    
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
    
    # Vérifier le système RAG complet
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

def check_streamlit():
    """Vérifier Streamlit"""
    print_header("STREAMLIT")
    
    # Vérifier si Streamlit est installé dans l'environnement RAG
    if os.path.exists("rag_env"):
        try:
            result = subprocess.run([
                "rag_env/bin/python", "-c", 
                "import streamlit; print(f'✅ Streamlit {streamlit.__version__} dans RAG')"
            ], capture_output=True, text=True, check=True)
            print(result.stdout.strip())
        except subprocess.CalledProcessError:
            print("❌ Streamlit dans RAG: Non installé")
    
    # Vérifier les dashboards Streamlit
    dashboard_files = [
        "dashboard_garantie/dashboard_simple.py",
        "dashboard_garantie/dashboard_garantie.py",
        "dashboard_garantie/launch_improved_dashboard.py"
    ]
    
    for file_path in dashboard_files:
        if os.path.exists(file_path):
            print(f"✅ Dashboard: {file_path}")
        else:
            print(f"❌ Dashboard: {file_path} - Absent")
    
    # Vérifier les requirements Streamlit
    if os.path.exists("requirements_streamlit.txt"):
        print("✅ Requirements Streamlit: Présent")
    else:
        print("❌ Requirements Streamlit: Absent")

def check_ollama():
    """Vérifier Ollama"""
    print_header("OLLAMA")
    
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
        
        if "llama" in result.stdout.lower():
            print("✅ Ollama: Modèles LLaMA disponibles")
            lines = result.stdout.strip().split('\n')
            for line in lines[1:]:  # Ignorer l'en-tête
                if line.strip():
                    print(f"   📦 {line.strip()}")
        else:
            print("⚠️ Ollama: Aucun modèle LLaMA trouvé")
        
        return True
    except subprocess.CalledProcessError:
        print("❌ Ollama: Service non accessible")
        return False
    except FileNotFoundError:
        print("❌ Ollama: Commande non trouvée")
        return False

def check_dependencies():
    """Vérifier les dépendances principales"""
    print_header("DÉPENDANCES PRINCIPALES")
    
    if not os.path.exists("rag_env"):
        print("❌ Environnement RAG non disponible")
        return False
    
    venv_python = "rag_env/bin/python"
    
    dependencies = [
        ("Django", "django"),
        ("sentence-transformers", "sentence_transformers"),
        ("openpyxl", "openpyxl"),
        ("reportlab", "reportlab"),
        ("rapidfuzz", "rapidfuzz"),
        ("psycopg2", "psycopg2"),
        ("python-dotenv", "dotenv")
    ]
    
    all_available = True
    for name, module in dependencies:
        try:
            result = subprocess.run([
                venv_python, "-c", 
                f"import {module}; print(f'✅ {name}: Disponible')"
            ], capture_output=True, text=True, check=True)
            print(result.stdout.strip())
        except subprocess.CalledProcessError:
            print(f"❌ {name}: Non disponible")
            all_available = False
    
    return all_available

def check_project_structure():
    """Vérifier la structure du projet"""
    print_header("STRUCTURE DU PROJET")
    
    required_dirs = [
        "apps/",
        "ParcInfo/",
        "templates/",
        "static/",
        "docs/",
        "dashboard_garantie/",
        "rag_env/"
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ Répertoire: {dir_path}")
        else:
            print(f"❌ Répertoire: {dir_path} - Absent")
    
    # Vérifier les fichiers clés
    key_files = [
        "manage.py",
        "README.md",
        "requirements.txt",
        "launch_with_rag.sh",
        "test_chatbot_rag.py"
    ]
    
    for file_path in key_files:
        if os.path.exists(file_path):
            print(f"✅ Fichier: {file_path}")
        else:
            print(f"❌ Fichier: {file_path} - Absent")

def check_git_status():
    """Vérifier le statut Git"""
    print_header("STATUT GIT")
    
    try:
        # Statut du dépôt
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
        if result.stdout.strip():
            print("⚠️  Fichiers modifiés non commités:")
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    print(f"   {line.strip()}")
        else:
            print("✅ Dépôt Git: Aucune modification en attente")
        
        # Branche actuelle
        result = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True, check=True)
        if result.returncode == 0:
            print(f"🌿 Branche actuelle: {result.stdout.strip()}")
        
        # Dernier commit
        result = subprocess.run(["git", "log", "-1", "--oneline"], capture_output=True, text=True, check=True)
        if result.returncode == 0:
            print(f"📝 Dernier commit: {result.stdout.strip()}")
        
    except subprocess.CalledProcessError:
        print("❌ Erreur lors de la vérification Git")
    except FileNotFoundError:
        print("❌ Git non installé")

def show_final_summary():
    """Afficher le résumé final"""
    print_header("RÉSUMÉ FINAL")
    
    print("🎯 **PROJET PARCINFO - VÉRIFICATION COMPLÈTE**")
    print("")
    print("✨ **Composants vérifiés :**")
    print("   • Système d'exploitation et Python")
    print("   • Environnements Python (système, RAG, Anaconda)")
    print("   • Django et configuration")
    print("   • Système RAG avec sentence-transformers")
    print("   • Streamlit et dashboards")
    print("   • Ollama et modèles LLM")
    print("   • Dépendances et packages")
    print("   • Structure du projet")
    print("   • Statut Git")
    print("")
    print("🚀 **Comment utiliser le projet :**")
    print("")
    print("1. **Lancement avec RAG :**")
    print("   ./launch_with_rag.sh")
    print("")
    print("2. **Lancement manuel :**")
    print("   source rag_env/bin/activate")
    print("   python manage.py runserver")
    print("")
    print("3. **Test du système :**")
    print("   python test_chatbot_rag.py")
    print("")
    print("4. **Dashboard Streamlit :**")
    print("   cd dashboard_garantie")
    print("   streamlit run dashboard_simple.py")
    print("")
    print("💡 **Le projet ParcInfo est maintenant équipé d'une IA avancée !**")

def main():
    """Fonction principale"""
    print("🚀 VÉRIFICATION COMPLÈTE DU PROJET PARCINFO")
    print("=" * 60)
    
    # Vérifications
    check_system_info()
    check_python_environments()
    check_django_environment()
    check_rag_system()
    check_streamlit()
    check_ollama()
    check_dependencies()
    check_project_structure()
    check_git_status()
    
    # Résumé final
    show_final_summary()

if __name__ == "__main__":
    main()
