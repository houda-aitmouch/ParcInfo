#!/usr/bin/env python3
"""
Script de diagnostic pour le Dashboard Garantie
"""

import os
import sys
import subprocess
import importlib

def check_environment():
    """Vérifie l'environnement"""
    print("🔍 Diagnostic de l'environnement...")
    print(f"📁 Répertoire actuel: {os.getcwd()}")
    print(f"🐍 Python version: {sys.version}")
    
    # Vérifier les fichiers
    files = [
        'dashboard_garantie.py',
        'custom_styles.css',
        'theme_config.py',
        'components.py'
    ]
    
    for file in files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MANQUANT")

def check_dependencies():
    """Vérifie les dépendances"""
    print("\n📦 Vérification des dépendances...")
    
    dependencies = [
        'streamlit',
        'plotly',
        'pandas',
        'django'
    ]
    
    for dep in dependencies:
        try:
            module = importlib.import_module(dep)
            version = getattr(module, '__version__', 'Version inconnue')
            print(f"✅ {dep} - {version}")
        except ImportError:
            print(f"❌ {dep} - NON INSTALLÉ")

def test_django_setup():
    """Teste la configuration Django"""
    print("\n🔧 Test de la configuration Django...")
    
    try:
        # Configuration Django
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
        
        import django
        django.setup()
        
        print("✅ Configuration Django réussie")
        
        # Test des modèles
        from apps.commande_bureau.models import CommandeBureau
        from apps.commande_informatique.models import Commande
        
        bureau_count = CommandeBureau.objects.count()
        info_count = Commande.objects.count()
        
        print(f"✅ Modèles accessibles - Bureau: {bureau_count}, Info: {info_count}")
        
    except Exception as e:
        print(f"❌ Erreur Django: {e}")

def test_streamlit_launch():
    """Teste le lancement de Streamlit"""
    print("\n🚀 Test de lancement Streamlit...")
    
    try:
        # Test de syntaxe
        result = subprocess.run([
            sys.executable, '-m', 'py_compile', 'dashboard_garantie.py'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Syntaxe Python valide")
        else:
            print(f"❌ Erreur de syntaxe: {result.stderr}")
            return False
        
        # Test de lancement rapide
        print("🔄 Test de lancement (5 secondes)...")
        process = subprocess.Popen([
            sys.executable, '-m', 'streamlit', 'run', 'dashboard_garantie.py',
            '--server.port', '8502',  # Port différent pour le test
            '--server.address', '0.0.0.0',
            '--server.headless', 'true'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        import time
        time.sleep(5)
        
        # Vérifier si le processus est toujours en cours
        if process.poll() is None:
            print("✅ Streamlit lancé avec succès")
            process.terminate()
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Erreur de lancement: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def main():
    """Fonction principale de diagnostic"""
    print("🔬 Diagnostic du Dashboard Garantie")
    print("=" * 50)
    
    check_environment()
    check_dependencies()
    test_django_setup()
    success = test_streamlit_launch()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Diagnostic terminé - Dashboard prêt à lancer")
        print("\n💡 Pour lancer le dashboard:")
        print("   streamlit run dashboard_garantie.py --server.port 8501")
    else:
        print("❌ Problèmes détectés - Vérifiez les erreurs ci-dessus")
        print("\n💡 Solutions possibles:")
        print("   1. Installer les dépendances manquantes")
        print("   2. Vérifier la configuration Django")
        print("   3. Corriger les erreurs de syntaxe")

if __name__ == "__main__":
    main()
