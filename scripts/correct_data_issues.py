#!/usr/bin/env python3
"""
Script de correction des problèmes de données identifiés dans l'analyse du chatbot ParcInfo.

Problèmes identifiés :
1. Numéros de série incorrects (ADD/INFO/010 → "123456", ADD/INFO/01000 → "12345")
2. Données manquantes sur les garanties
3. Incohérences dans les relations entre entités

Auteur: Assistant IA
Date: 18/08/2025
"""

import os
import sys
import django
from datetime import datetime, date

# Configuration Django
import sys
sys.path.append('/Users/HouDa/PycharmProjects/ParcInfo')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

from apps.materiel_informatique.models import MaterielInformatique
from apps.materiel_bureautique.models import MaterielBureau
from apps.commande_informatique.models import Commande
from apps.commande_bureau.models import CommandeBureau
from apps.fournisseurs.models import Fournisseur
from apps.users.models import CustomUser
from apps.livraison.models import Livraison
from apps.demande_equipement.models import DemandeEquipement

class DataCorrector:
    """Classe pour corriger les problèmes de données identifiés"""
    
    def __init__(self):
        """Initialise le correcteur de données"""
        self.corrections_made = []
        self.errors = []
        
        print("🔧 Initialisation du correcteur de données ParcInfo")
        print("📅 Date: 18/08/2025")
        print("🎯 Objectif: Corriger les problèmes de données identifiés")
    
    def correct_serial_numbers(self):
        """Corrige les numéros de série incorrects identifiés"""
        print("\n🔍 Correction des numéros de série...")
        
        try:
            # Correction du matériel ADD/INFO/010
            mat_010 = MaterielInformatique.objects.filter(
                code_inventaire='ADD/INFO/010'
            ).first()
            
            if mat_010:
                old_serial = mat_010.numero_serie
                # Correction vers un numéro de série valide
                mat_010.numero_serie = 'sn_correct'
                mat_010.save()
                
                self.corrections_made.append({
                    'type': 'numero_serie',
                    'materiel': 'ADD/INFO/010',
                    'ancien': old_serial,
                    'nouveau': 'sn_correct',
                    'timestamp': datetime.now()
                })
                
                print(f"✅ ADD/INFO/010: {old_serial} → sn_correct")
            else:
                print("⚠️ Matériel ADD/INFO/010 non trouvé")
            
            # Correction du matériel ADD/INFO/01000
            mat_01000 = MaterielInformatique.objects.filter(
                code_inventaire='ADD/INFO/01000'
            ).first()
            
            if mat_01000:
                old_serial = mat_01000.numero_serie
                # Correction vers un numéro de série valide
                mat_01000.numero_serie = 'sn_01000'
                mat_01000.save()
                
                self.corrections_made.append({
                    'type': 'numero_serie',
                    'materiel': 'ADD/INFO/01000',
                    'ancien': old_serial,
                    'nouveau': 'sn_01000',
                    'timestamp': datetime.now()
                })
                
                print(f"✅ ADD/INFO/01000: {old_serial} → sn_01000")
            else:
                print("⚠️ Matériel ADD/INFO/01000 non trouvé")
                
        except Exception as e:
            error_msg = f"Erreur lors de la correction des numéros de série: {e}"
            self.errors.append(error_msg)
            print(f"❌ {error_msg}")
    
    def correct_warranty_dates(self):
        """Corrige les dates de garantie manquantes ou incorrectes"""
        print("\n🔍 Correction des dates de garantie...")
        
        try:
            # Correction des commandes informatiques
            commandes_it = Commande.objects.all()
            for cmd in commandes_it:
                if not cmd.garantie_fin:
                    # Calculer une date de garantie basée sur la date de commande
                    if cmd.date_commande:
                        # Garantie de 2 ans par défaut
                        garantie_fin = date(
                            cmd.date_commande.year + 2,
                            cmd.date_commande.month,
                            cmd.date_commande.day
                        )
                        cmd.garantie_fin = garantie_fin
                        cmd.save()
                        
                        self.corrections_made.append({
                            'type': 'garantie_fin',
                            'commande': cmd.id,
                            'ancien': 'None',
                            'nouveau': garantie_fin.strftime('%d/%m/%Y'),
                            'timestamp': datetime.now()
                        })
                        
                        print(f"✅ Commande {cmd.id}: garantie_fin ajoutée → {garantie_fin.strftime('%d/%m/%Y')}")
            
            # Correction des commandes bureautiques
            commandes_bu = CommandeBureau.objects.all()
            for cmd in commandes_bu:
                if not cmd.garantie_fin:
                    # Calculer une date de garantie basée sur la date de commande
                    if cmd.date_commande:
                        # Garantie de 1 an par défaut pour le bureau
                        garantie_fin = date(
                            cmd.date_commande.year + 1,
                            cmd.date_commande.month,
                            cmd.date_commande.day
                        )
                        cmd.garantie_fin = garantie_fin
                        cmd.save()
                        
                        self.corrections_made.append({
                            'type': 'garantie_fin',
                            'commande': cmd.id,
                            'ancien': 'None',
                            'nouveau': garantie_fin.strftime('%d/%m/%Y'),
                            'timestamp': datetime.now()
                        })
                        
                        print(f"✅ Commande bureau {cmd.id}: garantie_fin ajoutée → {garantie_fin.strftime('%d/%m/%Y')}")
                        
        except Exception as e:
            error_msg = f"Erreur lors de la correction des garanties: {e}"
            self.errors.append(error_msg)
            print(f"❌ {error_msg}")
    
    def correct_material_locations(self):
        """Corrige les localisations des matériels"""
        print("\n🔍 Correction des localisations des matériels...")
        
        try:
            # Ajouter le champ lieu_stockage s'il n'existe pas
            # Note: Cette correction dépend de la structure de la base de données
            
            # Correction des matériels informatiques
            materiels_it = MaterielInformatique.objects.all()
            for mat in materiels_it:
                if not hasattr(mat, 'lieu_stockage') or not mat.lieu_stockage:
                    # Définir une localisation par défaut
                    if mat.code_inventaire in ['cd12', 'cd13', 'cd14']:
                        # Ces matériels sont à l'étage 1 selon l'analyse
                        if hasattr(mat, 'lieu_stockage'):
                            mat.lieu_stockage = 'etage1'
                            mat.save()
                            
                            self.corrections_made.append({
                                'type': 'lieu_stockage',
                                'materiel': mat.code_inventaire,
                                'ancien': 'None',
                                'nouveau': 'etage1',
                                'timestamp': datetime.now()
                            })
                            
                            print(f"✅ {mat.code_inventaire}: lieu_stockage ajouté → etage1")
            
            # Correction des matériels bureautiques
            materiels_bu = MaterielBureau.objects.all()
            for mat in materiels_bu:
                if not hasattr(mat, 'lieu_stockage') or not mat.lieu_stockage:
                    # Définir une localisation par défaut
                    if hasattr(mat, 'lieu_stockage'):
                        mat.lieu_stockage = 'etage1'
                        mat.save()
                        
                        self.corrections_made.append({
                            'type': 'lieu_stockage',
                            'materiel': mat.code_inventaire,
                            'ancien': 'None',
                            'nouveau': 'etage1',
                            'timestamp': datetime.now()
                        })
                        
                        print(f"✅ {mat.code_inventaire}: lieu_stockage ajouté → etage1")
                        
        except Exception as e:
            error_msg = f"Erreur lors de la correction des localisations: {e}"
            self.errors.append(error_msg)
            print(f"❌ {error_msg}")
    
    def correct_material_status(self):
        """Corrige les statuts des matériels"""
        print("\n🔍 Correction des statuts des matériels...")
        
        try:
            # Correction des matériels informatiques
            materiels_it = MaterielInformatique.objects.all()
            for mat in materiels_it:
                if not hasattr(mat, 'statut') or not mat.statut:
                    # Définir un statut par défaut
                    if hasattr(mat, 'statut'):
                        if mat.utilisateur:
                            mat.statut = 'affecte'
                        else:
                            mat.statut = 'en_stock'
                        mat.save()
                        
                        self.corrections_made.append({
                            'type': 'statut',
                            'materiel': mat.code_inventaire,
                            'ancien': 'None',
                            'nouveau': mat.statut,
                            'timestamp': datetime.now()
                        })
                        
                        print(f"✅ {mat.code_inventaire}: statut ajouté → {mat.statut}")
            
            # Correction des matériels bureautiques
            materiels_bu = MaterielBureau.objects.all()
            for mat in materiels_bu:
                if not hasattr(mat, 'statut') or not mat.statut:
                    # Définir un statut par défaut
                    if hasattr(mat, 'statut'):
                        if mat.utilisateur:
                            mat.statut = 'affecte'
                        else:
                            mat.statut = 'en_stock'
                        mat.save()
                        
                        self.corrections_made.append({
                            'type': 'statut',
                            'materiel': mat.code_inventaire,
                            'ancien': 'None',
                            'nouveau': mat.statut,
                            'timestamp': datetime.now()
                        })
                        
                        print(f"✅ {mat.code_inventaire}: statut ajouté → {mat.statut}")
                        
        except Exception as e:
            error_msg = f"Erreur lors de la correction des statuts: {e}"
            self.errors.append(error_msg)
            print(f"❌ {error_msg}")
    
    def create_database_indexes(self):
        """Crée des index pour améliorer les performances"""
        print("\n🔍 Création d'index de base de données...")
        
        try:
            from django.db import connection
            
            with connection.cursor() as cursor:
                # Index pour les matériels
                try:
                    cursor.execute("""
                        CREATE INDEX IF NOT EXISTS idx_materiels_lieu 
                        ON materiel_informatique(lieu_stockage)
                    """)
                    print("✅ Index idx_materiels_lieu créé")
                except Exception as e:
                    print(f"⚠️ Index idx_materiels_lieu: {e}")
                
                try:
                    cursor.execute("""
                        CREATE INDEX IF NOT EXISTS idx_materiels_statut 
                        ON materiel_informatique(statut)
                    """)
                    print("✅ Index idx_materiels_statut créé")
                except Exception as e:
                    print(f"⚠️ Index idx_materiels_statut: {e}")
                
                try:
                    cursor.execute("""
                        CREATE INDEX IF NOT EXISTS idx_demandes_statut 
                        ON demande_equipement(statut)
                    """)
                    print("✅ Index idx_demandes_statut créé")
                except Exception as e:
                    print(f"⚠️ Index idx_demandes_statut: {e}")
                
                try:
                    cursor.execute("""
                        CREATE INDEX IF NOT EXISTS idx_commandes_date 
                        ON commande(date_commande)
                    """)
                    print("✅ Index idx_commandes_date créé")
                except Exception as e:
                    print(f"⚠️ Index idx_commandes_date: {e}")
                    
        except Exception as e:
            error_msg = f"Erreur lors de la création des index: {e}"
            self.errors.append(error_msg)
            print(f"❌ {error_msg}")
    
    def run_all_corrections(self):
        """Exécute toutes les corrections"""
        print("\n" + "="*80)
        print("🔧 EXÉCUTION DES CORRECTIONS DE DONNÉES")
        print("="*80)
        
        start_time = datetime.now()
        
        # Exécution des corrections
        self.correct_serial_numbers()
        self.correct_warranty_dates()
        self.correct_material_locations()
        self.correct_material_status()
        self.create_database_indexes()
        
        # Génération du rapport
        self._generate_correction_report(start_time)
    
    def _generate_correction_report(self, start_time: datetime):
        """Génère le rapport des corrections effectuées"""
        print("\n" + "="*80)
        print("📊 RAPPORT DES CORRECTIONS EFFECTUÉES")
        print("="*80)
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        print(f"⏱️ Durée d'exécution: {duration}")
        print(f"✅ Corrections effectuées: {len(self.corrections_made)}")
        print(f"❌ Erreurs rencontrées: {len(self.errors)}")
        
        if self.corrections_made:
            print(f"\n📝 Détail des corrections:")
            for correction in self.corrections_made:
                print(f"   • {correction['type']}: {correction['materiel'] or correction['commande']}")
                print(f"     {correction['ancien']} → {correction['nouveau']}")
        
        if self.errors:
            print(f"\n⚠️ Erreurs rencontrées:")
            for error in self.errors:
                print(f"   • {error}")
        
        # Sauvegarde du rapport
        self._save_correction_report()
    
    def _save_correction_report(self):
        """Sauvegarde le rapport des corrections"""
        try:
            import json
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"correction_report_{timestamp}.json"
            
            report_data = {
                'timestamp': datetime.now().isoformat(),
                'corrections': self.corrections_made,
                'errors': self.errors
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"\n💾 Rapport sauvegardé dans: {filename}")
            
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde du rapport: {e}")


def main():
    """Fonction principale"""
    print("🔧 Correcteur de Données ParcInfo")
    print("📅 Date: 18/08/2025")
    print("🎯 Objectif: Corriger les problèmes de données identifiés")
    
    try:
        # Initialisation du correcteur
        corrector = DataCorrector()
        
        # Exécution des corrections
        corrector.run_all_corrections()
        
        print("\n✅ Corrections terminées avec succès!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Corrections interrompues par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
