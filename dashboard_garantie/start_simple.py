#!/usr/bin/env python3
"""
Script simple pour lancer le Dashboard Garantie
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
    
    # Lancer Streamlit
    print("📍 Dashboard accessible à: http://localhost:8501")
    print("🔄 Appuyez sur Ctrl+C pour arrêter")
    print()
    
    try:
        # Lancer Streamlit avec les paramètres de base
        cmd = [
            sys.executable, '-m', 'streamlit', 'run', 'dashboard_garantie.py',
            '--server.port', '8501',
            '--server.address', '0.0.0.0'
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
