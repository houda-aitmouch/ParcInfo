#!/usr/bin/env python
"""
Script d'archivage automatique des demandes signées
À exécuter quotidiennement via cron ou tâche planifiée
"""

import os
import sys
import django
from datetime import datetime

# Ajouter le répertoire parent au path Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

from django.core.management import call_command
from django.utils import timezone

def main():
    """Fonction principale d'archivage automatique"""
    print(f"🕐 Début de l'archivage automatique - {timezone.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # Exécuter la commande d'archivage
        call_command('archiver_demandes_signees')
        
        print("=" * 60)
        print(f"✅ Archivage automatique terminé - {timezone.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'archivage automatique: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 