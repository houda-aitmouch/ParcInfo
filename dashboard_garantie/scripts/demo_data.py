#!/usr/bin/env python3
"""
Script de génération de données de démonstration pour le Dashboard Garantie
Crée des commandes d'exemple avec des durées de garantie variées
"""

import os
import sys
import django
from datetime import date, timedelta
import random

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

from apps.commande_bureau.models import CommandeBureau, DesignationBureau, DescriptionBureau
from apps.commande_informatique.models import Commande, Designation, Description
from apps.fournisseurs.models import Fournisseur
from apps.users.models import CustomUser

def create_demo_data():
    """Crée des données de démonstration"""
    print("🎭 Création de données de démonstration...")
    
    # Créer des fournisseurs
    fournisseurs = []
    noms_fournisseurs = [
        "TechCorp Solutions", "OfficePlus Pro", "Digital Equipment Ltd",
        "Bureau Express", "Informatique Moderne", "Fournitures Pro"
    ]
    
    for nom in noms_fournisseurs:
        fournisseur, created = Fournisseur.objects.get_or_create(
            nom=nom,
            defaults={
                'adresse': f"Adresse de {nom}",
                'telephone': f"0{random.randint(100000000, 999999999)}",
                'email': f"contact@{nom.lower().replace(' ', '').replace('.', '')}.com"
            }
        )
        fournisseurs.append(fournisseur)
        if created:
            print(f"✅ Fournisseur créé: {nom}")
    
    # Créer des désignations et descriptions pour le bureau
    print("\n📋 Création des désignations bureautiques...")
    designations_bureau = []
    descriptions_bureau = []
    
    for i, nom in enumerate(['Mobilier', 'Éclairage', 'Décoration']):
        des, created = DesignationBureau.objects.get_or_create(nom=nom)
        designations_bureau.append(des)
        if created:
            print(f"✅ Désignation bureau créée: {nom}")
        
        for j in range(2):
            desc, created = DescriptionBureau.objects.get_or_create(
                nom=f"{nom} Type {j+1}",
                designation=des
            )
            descriptions_bureau.append(desc)
            if created:
                print(f"✅ Description bureau créée: {desc.nom}")
    
    # Créer des désignations et descriptions pour l'informatique
    print("\n💻 Création des désignations informatiques...")
    designations_info = []
    descriptions_info = []
    
    for i, nom in enumerate(['Ordinateurs', 'Périphériques', 'Réseau']):
        des, created = Designation.objects.get_or_create(nom=nom)
        designations_info.append(des)
        if created:
            print(f"✅ Désignation info créée: {nom}")
        
        for j in range(2):
            desc, created = Description.objects.get_or_create(
                nom=f"{nom} Modèle {j+1}",
                designation=des
            )
            descriptions_info.append(desc)
            if created:
                print(f"✅ Description info créée: {desc.nom}")
    
    # Créer des commandes bureautiques
    print("\n📋 Création des commandes bureautiques...")
    commandes_bureau = []
    
    for i in range(8):
        # Dates variées sur les 6 derniers mois
        date_commande = date.today() - timedelta(days=random.randint(30, 180))
        date_reception = date_commande + timedelta(days=random.randint(5, 15))
        
        # Durées de garantie variées
        duree_valeur = random.choice([6, 12, 18, 24])
        duree_unite = random.choice(['mois', 'annee'])
        
        commande = CommandeBureau.objects.create(
            mode_passation=random.choice(['BC', 'Contrat', 'AO']),
            numero_commande=f"CMD-BUR-{2024}-{i+1:03d}",
            fournisseur=random.choice(fournisseurs),
            date_commande=date_commande,
            date_reception=date_reception,
            numero_facture=f"FACT-{i+1:03d}",
            duree_garantie_valeur=duree_valeur,
            duree_garantie_unite=duree_unite
        )
        commandes_bureau.append(commande)
        print(f"✅ Commande bureau créée: {commande.numero_commande}")
    
    # Créer des commandes informatiques
    print("\n💻 Création des commandes informatiques...")
    commandes_info = []
    
    for i in range(10):
        # Dates variées sur les 6 derniers mois
        date_commande = date.today() - timedelta(days=random.randint(30, 180))
        date_reception = date_commande + timedelta(days=random.randint(5, 15))
        
        # Durées de garantie variées
        duree_valeur = random.choice([12, 24, 36, 48])
        duree_unite = random.choice(['mois', 'annee'])
        
        commande = Commande.objects.create(
            mode_passation=random.choice(['BC', 'Contrat', 'AO']),
            numero_commande=f"CMD-INFO-{2024}-{i+1:03d}",
            fournisseur=random.choice(fournisseurs),
            date_commande=date_commande,
            date_reception=date_reception,
            numero_facture=f"FACT-INFO-{i+1:03d}",
            duree_garantie_valeur=duree_valeur,
            duree_garantie_unite=duree_unite
        )
        commandes_info.append(commande)
        print(f"✅ Commande info créée: {commande.numero_commande}")
    
    print(f"\n🎉 Données de démonstration créées avec succès!")
    print(f"   - {len(fournisseurs)} fournisseurs")
    print(f"   - {len(designations_bureau)} désignations bureautiques")
    print(f"   - {len(designations_info)} désignations informatiques")
    print(f"   - {len(commandes_bureau)} commandes bureautiques")
    print(f"   - {len(commandes_info)} commandes informatiques")
    print(f"\n💡 Vous pouvez maintenant tester le dashboard avec ces données!")

def cleanup_demo_data():
    """Supprime les données de démonstration"""
    print("🧹 Nettoyage des données de démonstration...")
    
    # Supprimer les commandes
    CommandeBureau.objects.filter(numero_commande__startswith="CMD-BUR-").delete()
    Commande.objects.filter(numero_commande__startswith="CMD-INFO-").delete()
    
    # Supprimer les descriptions et désignations
    DescriptionBureau.objects.filter(nom__contains="Type").delete()
    Description.objects.filter(nom__contains="Modèle").delete()
    
    # Supprimer les fournisseurs de démo
    Fournisseur.objects.filter(nom__in=[
        "TechCorp Solutions", "OfficePlus Pro", "Digital Equipment Ltd",
        "Bureau Express", "Informatique Moderne", "Fournitures Pro"
    ]).delete()
    
    print("✅ Données de démonstration supprimées")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cleanup":
        cleanup_demo_data()
    else:
        create_demo_data()
        print("\n📋 Commandes disponibles:")
        print("  python demo_data.py              # Créer les données de démo")
        print("  python demo_data.py --cleanup    # Supprimer les données de démo")
