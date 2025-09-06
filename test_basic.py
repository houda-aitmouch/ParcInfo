#!/usr/bin/env python
"""
Test basique pour ParcInfo
Vérifie que les modules Django peuvent être importés
"""

import os
import sys
import django
from django.conf import settings

def test_django_setup():
    """Test de configuration Django"""
    try:
        # Configuration Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
        django.setup()
        
        # Test d'import des modèles
        from apps.users.models import CustomUser
        from apps.demande_equipement.models import DemandeEquipement
        from apps.chatbot.models import ChatbotInteraction
        
        print("✅ Django configuré correctement")
        print("✅ Modèles importés avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur Django: {e}")
        return False

def test_requirements():
    """Test des dépendances principales"""
    try:
        import django
        import psycopg2
        import numpy
        import pandas
        
        print("✅ Dépendances principales installées")
        return True
        
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Tests basiques ParcInfo")
    print("=" * 40)
    
    success = True
    
    # Test des dépendances
    if not test_requirements():
        success = False
    
    # Test Django
    if not test_django_setup():
        success = False
    
    print("=" * 40)
    if success:
        print("🎉 Tous les tests sont passés !")
        sys.exit(0)
    else:
        print("❌ Certains tests ont échoué")
        sys.exit(1)
