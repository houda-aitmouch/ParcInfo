#!/usr/bin/env python3
"""
Test des URLs pour les équipements informatiques superadmin
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

from django.urls import reverse
from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

def test_urls():
    """Test des URLs des équipements informatiques superadmin"""
    
    print("🧪 Test des URLs des équipements informatiques superadmin")
    print("=" * 60)
    
    # URLs à tester
    urls_to_test = [
        'materiel_informatique:liste_materiels_superadmin',
        'materiel_informatique:ajouter_materiel_superadmin',
        'materiel_informatique:export_excel_superadmin',
    ]
    
    # Test des URLs de base (sans paramètres)
    for url_name in urls_to_test:
        try:
            url = reverse(url_name)
            print(f"✅ {url_name}: {url}")
        except Exception as e:
            print(f"❌ {url_name}: Erreur - {e}")
    
    # Test des URLs avec paramètres
    urls_with_params = [
        ('materiel_informatique:modifier_materiel_superadmin', {'pk': 1}),
        ('materiel_informatique:confirmer_suppression_superadmin', {'pk': 1}),
    ]
    
    for url_name, kwargs in urls_with_params:
        try:
            url = reverse(url_name, kwargs=kwargs)
            print(f"✅ {url_name}: {url}")
        except Exception as e:
            print(f"❌ {url_name}: Erreur - {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Test des URLs terminé !")

if __name__ == '__main__':
    test_urls()
