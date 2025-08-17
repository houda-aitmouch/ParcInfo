#!/usr/bin/env python3
"""
🛡️ Moniteur Dashboard Garantie
========================================
Script de surveillance pour maintenir le dashboard Streamlit actif
"""

import subprocess
import time
import requests
import sys
import os
from datetime import datetime

def check_dashboard_status():
    """Vérifie si le dashboard Streamlit est accessible"""
    try:
        response = requests.get('http://localhost:8501', timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def start_dashboard():
    """Démarre le dashboard Streamlit"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🚀 Démarrage du dashboard Streamlit...")
    
    try:
        # Activer l'environnement virtuel et lancer le dashboard
        cmd = [
            sys.executable,  # Python de l'environnement actuel
            "launch_dashboard.py"
        ]
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Attendre un peu pour que le dashboard démarre
        time.sleep(10)
        
        if process.poll() is None:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Dashboard démarré avec succès (PID: {process.pid})")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Erreur lors du démarrage:")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return None
            
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Erreur: {e}")
        return None

def monitor_dashboard():
    """Moniteur principal du dashboard"""
    print("🛡️ Moniteur Dashboard Garantie")
    print("=" * 40)
    print("📊 Surveillance du dashboard Streamlit")
    print("🔄 Vérification toutes les 30 secondes")
    print("⏹️  Appuyez sur Ctrl+C pour arrêter")
    print("=" * 40)
    
    dashboard_process = None
    check_interval = 30  # secondes
    
    try:
        while True:
            current_time = datetime.now().strftime('%H:%M:%S')
            
            # Vérifier le statut du dashboard
            if check_dashboard_status():
                print(f"[{current_time}] ✅ Dashboard accessible")
            else:
                print(f"[{current_time}] ⚠️  Dashboard non accessible")
                
                # Arrêter l'ancien processus s'il existe
                if dashboard_process and dashboard_process.poll() is None:
                    print(f"[{current_time}] 🛑 Arrêt de l'ancien processus...")
                    dashboard_process.terminate()
                    dashboard_process.wait()
                
                # Redémarrer le dashboard
                dashboard_process = start_dashboard()
                
                if dashboard_process:
                    print(f"[{current_time}] 🔄 Dashboard redémarré")
                else:
                    print(f"[{current_time}] ❌ Échec du redémarrage")
            
            # Attendre avant la prochaine vérification
            time.sleep(check_interval)
            
    except KeyboardInterrupt:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🛑 Arrêt du moniteur...")
        
        # Arrêter le processus du dashboard
        if dashboard_process and dashboard_process.poll() is None:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 🛑 Arrêt du dashboard...")
            dashboard_process.terminate()
            dashboard_process.wait()
        
        print("✅ Moniteur arrêté")

def main():
    """Fonction principale"""
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        # Mode vérification simple
        if check_dashboard_status():
            print("✅ Dashboard accessible")
            sys.exit(0)
        else:
            print("❌ Dashboard non accessible")
            sys.exit(1)
    else:
        # Mode surveillance continue
        monitor_dashboard()

if __name__ == "__main__":
    main()
