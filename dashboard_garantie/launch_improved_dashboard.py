#!/usr/bin/env python3
"""
Script de lancement amélioré pour le Dashboard Garantie ParcInfo
Intègre toutes les améliorations de design et d'expérience utilisateur
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def print_banner():
    """Affiche une bannière de démarrage professionnelle"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║  🛡️  DASHBOARD GARANTIE PARCINFO - VERSION AMÉLIORÉE  🛡️   ║
    ║                                                              ║
    ║  Système de Surveillance et Gestion des Garanties          ║
    ║  Interface Professionnelle et Moderne                      ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_improvements():
    """Vérifie que toutes les améliorations sont en place"""
    print("🔍 Vérification des améliorations...")
    
    improvements = [
        ('custom_styles.css', 'Styles CSS personnalisés'),
        ('theme_config.py', 'Configuration des thèmes'),
        ('components.py', 'Composants réutilisables'),
        ('IMPROVEMENTS.md', 'Documentation des améliorations')
    ]
    
    all_present = True
    for file, description in improvements:
        if os.path.exists(file):
            print(f"✅ {description}")
        else:
            print(f"❌ {description} - {file} manquant")
            all_present = False
    
    return all_present

def check_dependencies():
    """Vérifie les dépendances requises"""
    print("\n📦 Vérification des dépendances...")
    
    try:
        import streamlit
        print(f"✅ Streamlit {streamlit.__version__}")
    except ImportError:
        print("❌ Streamlit non installé")
        return False
    
    try:
        import plotly
        print(f"✅ Plotly {plotly.__version__}")
    except ImportError:
        print("❌ Plotly non installé")
        return False
    
    try:
        import pandas
        print(f"✅ Pandas {pandas.__version__}")
    except ImportError:
        print("❌ Pandas non installé")
        return False
    
    return True

def setup_environment():
    """Configure l'environnement pour le dashboard"""
    print("\n⚙️ Configuration de l'environnement...")
    
    # Vérifier que nous sommes dans le bon répertoire
    if not os.path.exists('dashboard_garantie.py'):
        print("❌ Fichier dashboard_garantie.py non trouvé")
        print("💡 Assurez-vous d'exécuter ce script depuis le dossier dashboard_garantie/")
        return False
    
    # Vérifier la configuration Django
    if not os.path.exists('../manage.py'):
        print("⚠️ Fichier manage.py Django non trouvé")
        print("💡 Le dashboard peut ne pas fonctionner sans Django")
    
    print("✅ Environnement configuré")
    return True

def install_missing_dependencies():
    """Installe les dépendances manquantes"""
    print("\n📥 Installation des dépendances manquantes...")
    
    dependencies = [
        'streamlit',
        'plotly',
        'pandas',
        'django'
    ]
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep} déjà installé")
        except ImportError:
            print(f"📦 Installation de {dep}...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
                print(f"✅ {dep} installé avec succès")
            except subprocess.CalledProcessError:
                print(f"❌ Échec de l'installation de {dep}")
                return False
    
    return True

def launch_dashboard():
    """Lance le dashboard avec les améliorations"""
    print("\n🚀 Lancement du dashboard amélioré...")
    
    # Configuration Streamlit pour les améliorations
    env = os.environ.copy()
    env['STREAMLIT_SERVER_PORT'] = '8501'
    env['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
    env['STREAMLIT_SERVER_HEADLESS'] = 'true'
    env['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    
    # Commandes pour lancer Streamlit
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', 'dashboard_garantie.py',
        '--server.port', '8501',
        '--server.address', '0.0.0.0',
        '--server.headless', 'true',
        '--browser.gatherUsageStats', 'false'
    ]
    
    print("📍 Dashboard accessible à: http://localhost:8501")
    print("🔄 Appuyez sur Ctrl+C pour arrêter")
    print()
    
    try:
        # Ouvrir le navigateur automatiquement après un délai
        def open_browser():
            time.sleep(3)
            try:
                webbrowser.open('http://localhost:8501')
                print("🌐 Navigateur ouvert automatiquement")
            except:
                print("⚠️ Impossible d'ouvrir le navigateur automatiquement")
        
        # Lancer le dashboard
        process = subprocess.Popen(cmd, env=env)
        
        # Ouvrir le navigateur en arrière-plan
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Attendre que le processus se termine
        process.wait()
        
    except KeyboardInterrupt:
        print("\n👋 Arrêt du dashboard...")
        if 'process' in locals():
            process.terminate()
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        return False
    
    return True

def show_improvements_info():
    """Affiche les informations sur les améliorations"""
    print("\n🎨 Améliorations intégrées :")
    improvements = [
        "🎨 Design professionnel avec palette de couleurs cohérente",
        "📱 Interface responsive pour tous les appareils",
        "⚡ Animations et transitions fluides",
        "📊 Graphiques interactifs avec Plotly",
        "🔍 Filtres avancés et recherche",
        "📈 Métriques KPI avec indicateurs de tendance",
        "🚨 Système d'alertes intelligent",
        "♿ Accessibilité améliorée (WCAG 2.1)",
        "🎯 Navigation intuitive par onglets",
        "📋 Tableaux de données améliorés"
    ]
    
    for improvement in improvements:
        print(f"  {improvement}")
    
    print("\n💡 Fonctionnalités clés :")
    features = [
        "• Surveillance en temps réel des garanties",
        "• Alertes automatiques pour les expirations",
        "• Analyse par fournisseur et type d'équipement",
        "• Export de données et rapports",
        "• Gestion des rôles utilisateur",
        "• Interface adaptée à chaque profil"
    ]
    
    for feature in features:
        print(f"  {feature}")

def main():
    """Fonction principale"""
    print_banner()
    
    # Vérifications préliminaires
    if not check_improvements():
        print("\n⚠️ Certaines améliorations sont manquantes")
        print("💡 Exécutez d'abord le script d'amélioration")
        return False
    
    if not check_dependencies():
        print("\n📦 Installation des dépendances manquantes...")
        if not install_missing_dependencies():
            print("❌ Impossible d'installer toutes les dépendances")
            return False
    
    if not setup_environment():
        print("❌ Configuration de l'environnement échouée")
        return False
    
    # Afficher les informations sur les améliorations
    show_improvements_info()
    
    # Lancer le dashboard
    print("\n" + "="*60)
    print("🎯 Lancement du Dashboard Garantie Amélioré")
    print("="*60)
    
    success = launch_dashboard()
    
    if success:
        print("\n✅ Dashboard arrêté proprement")
    else:
        print("\n❌ Erreur lors de l'exécution du dashboard")
    
    return success

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Arrêt demandé par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur inattendue : {e}")
        sys.exit(1)
