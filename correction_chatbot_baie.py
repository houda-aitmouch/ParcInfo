#!/usr/bin/env python3
"""
Script de correction pour améliorer la gestion des requêtes sur les matériels "Baie"
dans le chatbot ParcInfo
"""

import os
import sys
import django
from django.db.models import Q

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

def test_baie_materials():
    """Teste la recherche des matériels 'Baie' dans la base de données"""
    print("🧪 Test de recherche des matériels 'Baie'")
    print("=" * 60)
    
    try:
        from apps.commande_informatique.models import LigneCommande, Designation, Description
        from apps.materiel_informatique.models import MaterielInformatique
        from apps.materiel_bureautique.models import MaterielBureau
        
        # 1. Recherche dans les lignes de commande
        print("1. Recherche dans les lignes de commande informatiques :")
        baie_lignes = LigneCommande.objects.filter(designation__nom__icontains='Baie')
        
        if baie_lignes.exists():
            print(f"   ✅ {baie_lignes.count()} ligne(s) de commande trouvée(s) pour 'Baie'")
            for ligne in baie_lignes:
                print(f"      - Commande : {ligne.commande.numero_commande}")
                print(f"        Désignation : {ligne.designation.nom}")
                print(f"        Description : {ligne.description.nom}")
                print(f"        Quantité : {ligne.quantite}")
                print(f"        Prix unitaire : {ligne.prix_unitaire}")
                print()
        else:
            print("   ❌ Aucune ligne de commande trouvée pour 'Baie'")
        
        # 2. Recherche dans les matériels informatiques
        print("2. Recherche dans les matériels informatiques :")
        baie_info = MaterielInformatique.objects.filter(
            Q(ligne_commande__designation__nom__icontains='Baie') |
            Q(ligne_commande__description__nom__icontains='Baie')
        ).select_related('ligne_commande__designation', 'ligne_commande__description', 'utilisateur')
        
        if baie_info.exists():
            print(f"   ✅ {baie_info.count()} matériel(s) informatique(s) trouvé(s) pour 'Baie'")
            for mat in baie_info:
                print(f"      - Code : {mat.code_inventaire}")
                print(f"        S/N : {mat.numero_serie}")
                print(f"        Affecté à : {mat.utilisateur.username if mat.utilisateur else 'Non affecté'}")
                if mat.ligne_commande:
                    print(f"        Désignation : {mat.ligne_commande.designation.nom}")
                    print(f"        Description : {mat.ligne_commande.description.nom}")
                print()
        else:
            print("   ❌ Aucun matériel informatique trouvé pour 'Baie'")
        
        # 3. Recherche dans les matériels bureautiques
        print("3. Recherche dans les matériels bureautiques :")
        baie_bureau = MaterielBureau.objects.filter(
            Q(ligne_commande__designation__nom__icontains='Baie') |
            Q(ligne_commande__description__nom__icontains='Baie')
        ).select_related('ligne_commande__designation', 'ligne_commande__description', 'utilisateur')
        
        if baie_bureau.exists():
            print(f"   ✅ {baie_bureau.count()} matériel(s) bureautique(s) trouvé(s) pour 'Baie'")
            for mat in baie_bureau:
                print(f"      - Code : {mat.code_inventaire}")
                print(f"        Affecté à : {mat.utilisateur.username if mat.utilisateur else 'Non affecté'}")
                if mat.ligne_commande:
                    print(f"        Désignation : {mat.ligne_commande.designation.nom}")
                    print(f"        Description : {mat.ligne_commande.description.nom}")
                print()
        else:
            print("   ❌ Aucun matériel bureautique trouvé pour 'Baie'")
        
        # 4. Analyse du problème
        print("4. Analyse du problème :")
        if baie_lignes.exists() and not baie_info.exists() and not baie_bureau.exists():
            print("   🔍 PROBLÈME IDENTIFIÉ :")
            print("      - Des 'Baies' existent dans les lignes de commande")
            print("      - Mais aucun matériel avec code d'inventaire n'est lié")
            print("      - Cela explique pourquoi le chatbot ne trouve pas de codes d'inventaire")
            print()
            print("   💡 SOLUTION PROPOSÉE :")
            print("      - Modifier la méthode _handle_codes_by_designation")
            print("      - Pour inclure les matériels des lignes de commande")
            print("      - Même s'ils n'ont pas de codes d'inventaire spécifiques")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        return False

def test_baie_commande_link():
    """Teste le lien entre les commandes et les matériels 'Baie'"""
    print("\n🧪 Test du lien entre commandes et matériels 'Baie'")
    print("=" * 60)
    
    try:
        from apps.commande_informatique.models import Commande, LigneCommande
        from apps.livraison.models import Livraison
        
        # Recherche des commandes avec des 'Baies'
        baie_commandes = Commande.objects.filter(
            lignes__designation__nom__icontains='Baie'
        ).distinct()
        
        if baie_commandes.exists():
            print(f"✅ {baie_commandes.count()} commande(s) trouvée(s) avec des 'Baies'")
            for cmd in baie_commandes:
                print(f"\n   📦 Commande : {cmd.numero_commande}")
                print(f"      Fournisseur : {cmd.fournisseur.nom}")
                print(f"      Date commande : {cmd.date_commande}")
                print(f"      Date réception : {cmd.date_reception}")
                print(f"      Durée garantie : {cmd.duree_garantie_valeur} {cmd.duree_garantie_unite}")
                
                # Lignes de commande pour cette commande
                lignes = cmd.lignes.filter(designation__nom__icontains='Baie')
                for ligne in lignes:
                    print(f"      - {ligne.designation.nom} : {ligne.description.nom}")
                    print(f"        Quantité : {ligne.quantite}, Prix : {ligne.prix_unitaire}")
                
                # Vérifier la livraison
                try:
                    livraison = Livraison.objects.get(numero_commande=cmd.numero_commande)
                    print(f"      📦 Livraison : {livraison.statut_livraison}")
                    print(f"        Prévu : {livraison.date_livraison_prevue}")
                    print(f"        Effectif : {livraison.date_livraison_effective}")
                    if livraison.date_livraison_effective and livraison.date_livraison_prevue:
                        retard = (livraison.date_livraison_effective - livraison.date_livraison_prevue).days
                        if retard > 0:
                            print(f"        ⚠️ Retard : {retard} jours")
                except Livraison.DoesNotExist:
                    print(f"      📦 Livraison : Non trouvée")
        else:
            print("❌ Aucune commande trouvée avec des 'Baies'")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        return False

def propose_solution():
    """Propose une solution pour corriger le problème"""
    print("\n🔧 PROPOSITION DE SOLUTION")
    print("=" * 60)
    
    print("Le problème principal est que la méthode _handle_codes_by_designation")
    print("ne trouve pas de codes d'inventaire pour les 'Baies' car :")
    print()
    print("1. Les 'Baies' existent dans les lignes de commande (BC23, BC24)")
    print("2. Mais aucun matériel avec code d'inventaire n'est lié à ces lignes")
    print("3. Le chatbot cherche dans MaterielInformatique et MaterielBureau")
    print()
    print("SOLUTIONS PROPOSÉES :")
    print()
    print("A. CORRECTION IMMÉDIATE (Recommandée) :")
    print("   Modifier _handle_codes_by_designation pour inclure les matériels")
    print("   des lignes de commande même sans codes d'inventaire")
    print()
    print("B. CORRECTION STRUCTURELLE :")
    print("   Créer des matériels avec codes d'inventaire pour chaque 'Baie'")
    print("   et les lier aux lignes de commande correspondantes")
    print()
    print("C. AMÉLIORATION DE LA RÉPONSE :")
    print("   Quand aucun code d'inventaire n'est trouvé, afficher les")
    print("   informations des lignes de commande comme alternative")
    
    return True

def main():
    """Fonction principale"""
    print("🚀 CORRECTION DU CHATBOT - PROBLÈME DES MATÉRIELS 'BAIE'")
    print("=" * 70)
    
    # Tests
    test1 = test_baie_materials()
    test2 = test_baie_commande_link()
    propose_solution()
    
    # Résumé
    print("\n📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    successful = sum([test1, test2])
    total = 2
    
    print(f"✅ Tests réussis : {successful}/{total}")
    print(f"❌ Tests échoués : {total - successful}/{total}")
    
    if successful == total:
        print("\n🎯 PROCHAINES ÉTAPES :")
        print("1. Implémenter la correction A (immédiate)")
        print("2. Tester avec le chatbot")
        print("3. Évaluer si la correction B est nécessaire")
        print("4. Documenter les changements")
    else:
        print("\n⚠️ Des tests ont échoué. Vérifiez la configuration Django.")

if __name__ == "__main__":
    main()
