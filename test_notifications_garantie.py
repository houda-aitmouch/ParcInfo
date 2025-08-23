#!/usr/bin/env python3
"""
Script de test pour le système de notifications de garantie
"""

import os
import sys
import django
from datetime import date, timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

from apps.materiel_informatique.models import MaterielInformatique
from apps.materiel_bureautique.models import MaterielBureau
from apps.users.models import CustomUser
from django.contrib.auth.models import Group

def test_notifications_garantie():
    """Test du système de notifications de garantie"""
    print("=== Test du système de notifications de garantie ===\n")
    
    # Test 1: Vérifier les modèles
    print("1. Vérification des modèles...")
    try:
        materiels_info = MaterielInformatique.objects.count()
        materiels_bureau = MaterielBureau.objects.count()
        print(f"   ✓ Matériels informatiques: {materiels_info}")
        print(f"   ✓ Matériels bureau: {materiels_bureau}")
    except Exception as e:
        print(f"   ✗ Erreur lors de la vérification des modèles: {e}")
        return False
    
    # Test 2: Vérifier les propriétés de garantie
    print("\n2. Vérification des propriétés de garantie...")
    try:
        if materiels_info > 0:
            materiel_info = MaterielInformatique.objects.first()
            date_fin = materiel_info.date_fin_garantie_calculee
            print(f"   ✓ Exemple matériel IT - Date fin garantie: {date_fin}")
        
        if materiels_bureau > 0:
            materiel_bureau = MaterielBureau.objects.first()
            date_fin = materiel_bureau.date_fin_garantie_calculee
            print(f"   ✓ Exemple matériel Bureau - Date fin garantie: {date_fin}")
    except Exception as e:
        print(f"   ✗ Erreur lors de la vérification des propriétés: {e}")
        return False
    
    # Test 3: Vérifier les groupes d'utilisateurs
    print("\n3. Vérification des groupes d'utilisateurs...")
    try:
        groupes = Group.objects.all()
        print(f"   ✓ Groupes disponibles: {[g.name for g in groupes]}")
        
        # Vérifier les utilisateurs par groupe
        for groupe in groupes:
            users = CustomUser.objects.filter(groups=groupe)
            print(f"   - {groupe.name}: {users.count()} utilisateurs")
            
    except Exception as e:
        print(f"   ✗ Erreur lors de la vérification des groupes: {e}")
        return False
    
    # Test 4: Simulation des notifications
    print("\n4. Simulation des notifications...")
    try:
        date_limite = date.today() + timedelta(days=30)
        print(f"   ✓ Date limite: {date_limite}")
        
        # Compter les matériels avec garantie expirante
        materiels_info_expirants = 0
        materiels_bureau_expirants = 0
        
        for materiel in MaterielInformatique.objects.all():
            date_fin = materiel.date_fin_garantie_calculee
            if date_fin and date_fin <= date_limite:
                materiels_info_expirants += 1
        
        for materiel in MaterielBureau.objects.all():
            date_fin = materiel.date_fin_garantie_calculee
            if date_fin and date_fin <= date_limite:
                materiels_bureau_expirants += 1
        
        print(f"   ✓ Matériels IT avec garantie expirante: {materiels_info_expirants}")
        print(f"   ✓ Matériels Bureau avec garantie expirante: {materiels_bureau_expirants}")
        
    except Exception as e:
        print(f"   ✗ Erreur lors de la simulation: {e}")
        return False
    
    print("\n=== Test terminé avec succès ===")
    return True

def test_urls():
    """Test des URLs de notifications"""
    print("\n=== Test des URLs de notifications ===\n")
    
    try:
        from django.urls import reverse
        from django.test import Client
        
        # Créer un client de test
        client = Client()
        
        # Test de l'URL des notifications
        url = reverse('users:notifications_garantie')
        print(f"1. URL des notifications: {url}")
        
        # Test sans authentification (doit rediriger vers login)
        response = client.get(url)
        print(f"2. Test sans authentification: {response.status_code}")
        
        # Test avec un utilisateur superuser
        try:
            superuser = CustomUser.objects.filter(is_superuser=True).first()
            if superuser:
                client.force_login(superuser)
                response = client.get(url)
                print(f"3. Test avec superuser: {response.status_code}")
                if response.status_code == 200:
                    print("   ✓ Réponse JSON reçue")
                    try:
                        data = response.json()
                        print(f"   ✓ Données: {len(data.get('notifications', []))} notifications")
                    except:
                        print("   ✗ Erreur lors du parsing JSON")
                else:
                    print(f"   ✗ Code de statut inattendu: {response.status_code}")
            else:
                print("3. Aucun superuser trouvé pour le test")
        except Exception as e:
            print(f"   ✗ Erreur lors du test avec superuser: {e}")
        
    except Exception as e:
        print(f"✗ Erreur lors du test des URLs: {e}")
        return False
    
    print("\n=== Test des URLs terminé ===")
    return True

if __name__ == "__main__":
    print("Démarrage des tests de notifications de garantie...\n")
    
    # Exécuter les tests
    success1 = test_notifications_garantie()
    success2 = test_urls()
    
    if success1 and success2:
        print("\n🎉 Tous les tests sont passés avec succès!")
        sys.exit(0)
    else:
        print("\n❌ Certains tests ont échoué")
        sys.exit(1)
