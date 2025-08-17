#!/usr/bin/env python3
"""
Script de test pour le Dashboard Garantie ParcInfo
Vérifie que tous les composants nécessaires sont en place
"""

import os
import sys
import django
from django.conf import settings
from django.db import connection

def test_django_setup():
    """Teste la configuration Django"""
    print("🔧 Test de la configuration Django...")
    
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
        django.setup()
        print("✅ Django configuré avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur de configuration Django: {e}")
        return False

def test_database_connection():
    """Teste la connexion à la base de données"""
    print("🗄️ Test de la connexion à la base de données...")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Connexion à la base de données réussie")
            return True
    except Exception as e:
        print(f"❌ Erreur de connexion à la base de données: {e}")
        return False

def test_models_import():
    """Teste l'import des modèles"""
    print("📦 Test de l'import des modèles...")
    
    try:
        from apps.commande_bureau.models import CommandeBureau
        from apps.commande_informatique.models import Commande
        from apps.fournisseurs.models import Fournisseur
        from apps.users.models import CustomUser
        print("✅ Modèles importés avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur d'import des modèles: {e}")
        return False

def test_data_availability():
    """Teste la disponibilité des données"""
    print("📊 Test de la disponibilité des données...")
    
    try:
        from apps.commande_bureau.models import CommandeBureau
        from apps.commande_informatique.models import Commande
        from apps.fournisseurs.models import Fournisseur
        from apps.users.models import CustomUser
        
        # Compter les enregistrements
        nb_commandes_bureau = CommandeBureau.objects.count()
        nb_commandes_info = Commande.objects.count()
        nb_fournisseurs = Fournisseur.objects.count()
        nb_users = CustomUser.objects.count()
        
        print(f"✅ Données disponibles:")
        print(f"   - Commandes bureau: {nb_commandes_bureau}")
        print(f"   - Commandes informatiques: {nb_commandes_info}")
        print(f"   - Fournisseurs: {nb_fournisseurs}")
        print(f"   - Utilisateurs: {nb_users}")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la vérification des données: {e}")
        return False

def test_permissions():
    """Teste la configuration des permissions"""
    print("🔐 Test de la configuration des permissions...")
    
    try:
        from django.contrib.auth.models import Group
        
        groups = Group.objects.all()
        print(f"✅ Groupes disponibles: {[g.name for g in groups]}")
        
        # Vérifier les groupes essentiels
        essential_groups = ['Super Admin', 'Gestionnaire Informatique', 'Gestionnaire Bureau', 'Employe']
        existing_groups = [g.name for g in groups]
        
        missing_groups = [g for g in essential_groups if g not in existing_groups]
        if missing_groups:
            print(f"⚠️ Groupes manquants: {missing_groups}")
        else:
            print("✅ Tous les groupes essentiels sont présents")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la vérification des permissions: {e}")
        return False

def test_streamlit_dependencies():
    """Teste les dépendances Streamlit"""
    print("📱 Test des dépendances Streamlit...")
    
    try:
        import streamlit as st
        import pandas as pd
        import plotly.express as px
        
        print("✅ Dépendances Streamlit disponibles")
        return True
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("💡 Installez les dépendances avec: pip install -r requirements_streamlit.txt")
        return False

def main():
    """Fonction principale de test"""
    print("🧪 Test du Dashboard Garantie ParcInfo")
    print("=" * 50)
    
    tests = [
        ("Configuration Django", test_django_setup),
        ("Connexion Base de Données", test_database_connection),
        ("Import des Modèles", test_models_import),
        ("Disponibilité des Données", test_data_availability),
        ("Configuration des Permissions", test_permissions),
        ("Dépendances Streamlit", test_streamlit_dependencies),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur lors du test: {e}")
            results.append((test_name, False))
    
    # Résumé des tests
    print("\n" + "=" * 50)
    print("📋 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Résultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés! Le dashboard est prêt à être lancé.")
        print("🚀 Lancez le dashboard avec: ./launch_dashboard.sh")
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez la configuration avant de lancer le dashboard.")
        print("💡 Consultez le README_DASHBOARD.md pour plus d'informations.")

if __name__ == "__main__":
    main()
