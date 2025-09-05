#!/usr/bin/env python3
"""
Script de diagnostic pour ParcInfo
"""

import os
import sys
import django
from django.conf import settings

def main():
    print("🔍 DIAGNOSTIC PARCINFO")
    print("=" * 50)
    
    # 1. Vérifier Python
    print(f"✅ Python version: {sys.version}")
    
    # 2. Vérifier l'environnement
    print(f"✅ Environnement virtuel: {os.environ.get('VIRTUAL_ENV', 'Non activé')}")
    
    # 3. Vérifier Django
    try:
        import django
        print(f"✅ Django version: {django.get_version()}")
    except ImportError as e:
        print(f"❌ Django non disponible: {e}")
        return
    
    # 4. Configurer Django
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
        django.setup()
        print("✅ Configuration Django chargée")
    except Exception as e:
        print(f"❌ Erreur configuration Django: {e}")
        return
    
    # 5. Vérifier la base de données
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ Base de données connectée: {version[0]}")
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")
        return
    
    # 6. Vérifier les applications
    try:
        from django.apps import apps
        print(f"✅ Applications installées: {len(apps.get_app_configs())}")
    except Exception as e:
        print(f"❌ Erreur applications: {e}")
        return
    
    # 7. Vérifier les URLs
    try:
        from django.urls import get_resolver
        resolver = get_resolver()
        print(f"✅ URLs configurées: {len(resolver.url_patterns)}")
    except Exception as e:
        print(f"❌ Erreur URLs: {e}")
        return
    
    print("\n🎉 Diagnostic terminé - Tout semble correct !")
    print("💡 Vous pouvez maintenant lancer le serveur avec: python manage.py runserver")

if __name__ == "__main__":
    main()
