#!/usr/bin/env python3
"""
Script de lancement simple du Dashboard Garantie
Exécutez ce script depuis le dossier racine du projet
"""

import sys
import os

# Ajouter le dossier dashboard_garantie au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dashboard_garantie'))

# Importer et exécuter le script principal
from run_dashboard import main

if __name__ == "__main__":
    main()
