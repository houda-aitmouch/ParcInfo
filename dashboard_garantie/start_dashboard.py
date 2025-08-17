#!/usr/bin/env python3
"""
Script de lancement simplifié pour le Dashboard Garantie
"""

import os
import sys
import subprocess
import time

def main():
    print("🚀 Lancement du Dashboard Garantie...")
    
    # Vérifier que nous sommes dans le bon répertoire
    if not os.path.exists('dashboard_garantie.py'):
        print("❌ Fichier dashboard_garantie.py non trouvé")
        print("💡 Assurez-vous d'être dans le dossier dashboard_garantie/")
        return False
    
    # Vérifier les dépendances
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
    
    # Lancer Streamlit
    print("📍 Lancement du dashboard...")
    print("📍 Accessible à: http://localhost:8501")
    print("🔄 Appuyez sur Ctrl+C pour arrêter")
    print()
    
    try:
        # Lancer Streamlit avec les paramètres optimaux
        cmd = [
            sys.executable, '-m', 'streamlit', 'run', 'dashboard_garantie.py',
            '--server.port', '8501',
            '--server.address', '0.0.0.0',
            '--browser.gatherUsageStats', 'false',
            '--server.headless', 'true'
        ]
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n👋 Dashboard arrêté")
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
