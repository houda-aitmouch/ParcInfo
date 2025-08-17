#!/usr/bin/env python3
"""
Script principal pour lancer le Dashboard Garantie ParcInfo
Ce script peut être exécuté depuis le dossier racine du projet
"""

import os
import sys
import subprocess
import argparse

def check_environment():
    """Vérifie que l'environnement est correctement configuré"""
    print("🔍 Vérification de l'environnement...")
    
    # Vérifier si on est dans le bon répertoire
    if not os.path.exists('manage.py'):
        print("❌ Erreur: Ce script doit être exécuté depuis le dossier racine du projet ParcInfo")
        print("💡 Assurez-vous d'être dans le dossier contenant manage.py")
        return False
    
    # Vérifier si l'environnement virtuel existe
    if not os.path.exists('env'):
        print("⚠️ Environnement virtuel non trouvé")
        print("💡 Créez l'environnement virtuel avec: python3 -m venv env")
        return False
    
    print("✅ Environnement vérifié")
    return True

def install_dependencies():
    """Installe les dépendances"""
    print("📦 Installation des dépendances...")
    
    try:
        # Activer l'environnement virtuel et installer les dépendances
        if os.name == 'nt':  # Windows
            activate_script = os.path.join('env', 'Scripts', 'activate.bat')
            cmd = f'call "{activate_script}" && pip install -r requirements.txt'
            subprocess.run(cmd, shell=True, check=True)
        else:  # Linux/macOS
            activate_script = os.path.join('env', 'bin', 'activate')
            cmd = f'source "{activate_script}" && pip install -r requirements.txt'
            subprocess.run(cmd, shell=True, check=True)
        
        print("✅ Dépendances installées")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'installation: {e}")
        return False

def run_dashboard():
    """Lance le dashboard"""
    print("🚀 Lancement du dashboard...")
    
    try:
        # Aller dans le dossier dashboard_garantie
        os.chdir('dashboard_garantie')
        
        # Lancer Streamlit
        cmd = [
            sys.executable, '-m', 'streamlit', 'run', 'dashboard_garantie.py',
            '--server.port', '8501',
            '--server.address', '0.0.0.0'
        ]
        
        print("📍 Dashboard accessible à: http://localhost:8501")
        print("🔄 Appuyez sur Ctrl+C pour arrêter")
        print()
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n👋 Dashboard arrêté")
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        return False
    
    return True

def create_users():
    """Crée les utilisateurs de démonstration"""
    print("👥 Création des utilisateurs de démonstration...")
    
    try:
        script_path = os.path.join('dashboard_garantie', 'scripts', 'create_users.py')
        subprocess.run([sys.executable, script_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la création des utilisateurs: {e}")
        return False

def create_demo_data():
    """Crée les données de démonstration"""
    print("🎭 Création des données de démonstration...")
    
    try:
        script_path = os.path.join('dashboard_garantie', 'scripts', 'demo_data.py')
        subprocess.run([sys.executable, script_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la création des données: {e}")
        return False

def test_configuration():
    """Teste la configuration"""
    print("🧪 Test de la configuration...")
    
    try:
        script_path = os.path.join('dashboard_garantie', 'scripts', 'test_dashboard.py')
        subprocess.run([sys.executable, script_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description='Dashboard Garantie ParcInfo')
    parser.add_argument('--install', action='store_true', help='Installer les dépendances')
    parser.add_argument('--test', action='store_true', help='Tester la configuration')
    parser.add_argument('--users', action='store_true', help='Créer les utilisateurs de démo')
    parser.add_argument('--data', action='store_true', help='Créer les données de démo')
    parser.add_argument('--setup', action='store_true', help='Configuration complète (install + users + data)')
    
    args = parser.parse_args()
    
    print("🛡️ Dashboard Garantie ParcInfo")
    print("=" * 40)
    
    # Vérifier l'environnement
    if not check_environment():
        return
    
    # Configuration complète
    if args.setup:
        print("🔧 Configuration complète...")
        if install_dependencies():
            create_users()
            create_demo_data()
        return
    
    # Installation des dépendances
    if args.install:
        install_dependencies()
        return
    
    # Test de configuration
    if args.test:
        test_configuration()
        return
    
    # Création des utilisateurs
    if args.users:
        create_users()
        return
    
    # Création des données
    if args.data:
        create_demo_data()
        return
    
    # Lancement du dashboard (par défaut)
    if not any([args.install, args.test, args.users, args.data, args.setup]):
        print("💡 Utilisez --help pour voir toutes les options")
        print("🚀 Lancement du dashboard...")
        run_dashboard()

if __name__ == "__main__":
    main()
