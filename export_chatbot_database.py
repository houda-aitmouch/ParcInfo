#!/usr/bin/env python3
"""
Script d'export complet de la base de données des modèles utilisés par le chatbot
Génère un fichier TXT avec toutes les données structurées
"""

import os
import sys
import django
from datetime import datetime
from django.db import connection
from django.core.serializers import serialize

# Configuration Django
sys.path.append('/Users/HouDa/PycharmProjects/ParcInfo')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

# Import de tous les modèles utilisés par le chatbot
from apps.materiel_informatique.models import MaterielInformatique
from apps.materiel_bureautique.models import MaterielBureau
from apps.commande_informatique.models import Commande, LigneCommande, Designation, Description
from apps.commande_bureau.models import CommandeBureau, LigneCommandeBureau, DesignationBureau, DescriptionBureau
from apps.fournisseurs.models import Fournisseur
from apps.users.models import CustomUser
from apps.livraison.models import Livraison
from apps.demande_equipement.models import DemandeEquipement, ArchiveDecharge, Fourniture
from apps.chatbot.models import IntentExample, ChatbotFeedback, ChatbotInteraction
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class ChatbotDatabaseExporter:
    """Exportateur complet de la base de données pour le chatbot"""
    
    def __init__(self):
        self.output_file = f"export_chatbot_database_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        self.total_records = 0
        
    def export_all_data(self):
        """Exporte toutes les données des modèles utilisés par le chatbot"""
        
        print("🚀 DÉBUT DE L'EXPORT DE LA BASE DE DONNÉES CHATBOT")
        print("=" * 80)
        print(f"📅 Date d'export : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 Fichier de sortie : {self.output_file}")
        print()
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            # En-tête du fichier
            f.write("=" * 80 + "\n")
            f.write("EXPORT COMPLET DE LA BASE DE DONNÉES - MODÈLES CHATBOT\n")
            f.write("=" * 80 + "\n")
            f.write(f"Date d'export : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Généré par : Script d'export automatique\n")
            f.write("=" * 80 + "\n\n")
            
            # Export de chaque modèle
            self._export_model(f, "UTILISATEURS", CustomUser, [
                'id', 'username', 'email', 'first_name', 'last_name', 
                'is_active', 'is_staff', 'is_superuser', 'date_joined'
            ])
            
            self._export_model(f, "GROUPES", Group, [
                'id', 'name', 'permissions'
            ])
            
            self._export_model(f, "PERMISSIONS", Permission, [
                'id', 'name', 'content_type', 'codename'
            ])
            
            self._export_model(f, "FOURNISSEURS", Fournisseur, [
                'id', 'nom', 'adresse', 'telephone', 'email', 'contact_principal'
            ])
            
            self._export_model(f, "DESIGNATIONS INFORMATIQUE", Designation, [
                'id', 'nom'
            ])
            
            self._export_model(f, "DESCRIPTIONS INFORMATIQUE", Description, [
                'id', 'nom'
            ])
            
            self._export_model(f, "COMMANDES INFORMATIQUE", Commande, [
                'id', 'numero_commande', 'date_commande', 'fournisseur', 'montant_total', 'statut'
            ])
            
            self._export_model(f, "LIGNES COMMANDE INFORMATIQUE", LigneCommande, [
                'id', 'commande', 'designation', 'description', 'quantite', 'prix_unitaire', 'montant_total'
            ])
            
            self._export_model(f, "MATÉRIELS INFORMATIQUE", MaterielInformatique, [
                'id', 'code_inventaire', 'numero_serie', 'designation', 'description',
                'statut', 'utilisateur', 'ligne_commande', 'date_affectation', 'date_fin_garantie_calculee'
            ])
            
            self._export_model(f, "DESIGNATIONS BUREAUTIQUE", DesignationBureau, [
                'id', 'nom'
            ])
            
            self._export_model(f, "DESCRIPTIONS BUREAUTIQUE", DescriptionBureau, [
                'id', 'nom'
            ])
            
            self._export_model(f, "COMMANDES BUREAUTIQUE", CommandeBureau, [
                'id', 'numero_commande', 'date_commande', 'fournisseur', 'montant_total', 'statut'
            ])
            
            self._export_model(f, "LIGNES COMMANDE BUREAUTIQUE", LigneCommandeBureau, [
                'id', 'commande', 'designation', 'description', 'quantite', 'prix_unitaire', 'montant_total'
            ])
            
            self._export_model(f, "MATÉRIELS BUREAUTIQUE", MaterielBureau, [
                'id', 'code_inventaire', 'designation', 'description',
                'statut', 'utilisateur', 'ligne_commande', 'date_affectation', 'date_fin_garantie_calculee'
            ])
            
            self._export_model(f, "LIVRAISONS", Livraison, [
                'id', 'numero_livraison', 'date_livraison', 'fournisseur', 'statut', 'commentaires'
            ])
            
            self._export_model(f, "DEMANDES D'ÉQUIPEMENT", DemandeEquipement, [
                'id', 'demandeur', 'categorie', 'type_article', 'type_demande',
                'statut', 'date_demande', 'date_approbation', 'designation_info', 'description_info'
            ])
            
            self._export_model(f, "FOURNITURES", Fourniture, [
                'id', 'demande', 'designation', 'description', 'quantite', 'prix_unitaire'
            ])
            
            self._export_model(f, "ARCHIVES DÉCHARGE", ArchiveDecharge, [
                'id', 'demande', 'date_signature', 'fichier_decharge', 'statut'
            ])
            
            self._export_model(f, "EXEMPLES D'INTENTIONS CHATBOT", IntentExample, [
                'id', 'intent', 'example_text', 'created_at'
            ])
            
            self._export_model(f, "FEEDBACK CHATBOT", ChatbotFeedback, [
                'id', 'user', 'interaction_id', 'rating', 'comment', 'created_at'
            ])
            
            self._export_model(f, "INTERACTIONS CHATBOT", ChatbotInteraction, [
                'id', 'user', 'query', 'response', 'intent', 'confidence', 'created_at'
            ])
            
            # Statistiques finales
            f.write("\n" + "=" * 80 + "\n")
            f.write("STATISTIQUES D'EXPORT\n")
            f.write("=" * 80 + "\n")
            f.write(f"Total d'enregistrements exportés : {self.total_records}\n")
            f.write(f"Date de fin d'export : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n")
        
        print(f"✅ Export terminé avec succès !")
        print(f"📁 Fichier généré : {self.output_file}")
        print(f"📊 Total d'enregistrements : {self.total_records}")
        
    def _export_model(self, file, model_name, model_class, fields):
        """Exporte les données d'un modèle spécifique"""
        
        print(f"📋 Export de {model_name}...")
        
        try:
            # Compter les enregistrements
            count = model_class.objects.count()
            self.total_records += count
            
            file.write(f"\n{'=' * 60}\n")
            file.write(f"MODÈLE : {model_name}\n")
            file.write(f"{'=' * 60}\n")
            file.write(f"Nombre d'enregistrements : {count}\n")
            file.write(f"Champs exportés : {', '.join(fields)}\n")
            file.write(f"{'=' * 60}\n\n")
            
            if count == 0:
                file.write("Aucun enregistrement trouvé.\n\n")
                print(f"   ⚠️  Aucun enregistrement pour {model_name}")
                return
            
            # En-têtes des colonnes
            file.write(" | ".join(fields) + "\n")
            file.write("-" * (len(" | ".join(fields)) + 10) + "\n")
            
            # Export des données
            for obj in model_class.objects.all()[:1000]:  # Limite à 1000 pour éviter les fichiers trop volumineux
                row_data = []
                for field in fields:
                    try:
                        value = getattr(obj, field)
                        if hasattr(value, 'pk'):  # ForeignKey
                            value = f"{value.__class__.__name__}(id={value.pk})"
                        elif hasattr(value, 'all'):  # ManyToManyField
                            related_objects = list(value.all()[:5])  # Limite à 5
                            value = f"[{', '.join([f'{obj.__class__.__name__}(id={obj.pk})' for obj in related_objects])}]"
                        elif isinstance(value, datetime):
                            value = value.strftime('%Y-%m-%d %H:%M:%S')
                        elif value is None:
                            value = "NULL"
                        else:
                            value = str(value)
                        
                        # Limiter la longueur pour la lisibilité
                        if len(value) > 50:
                            value = value[:47] + "..."
                        
                        row_data.append(value)
                    except Exception as e:
                        row_data.append(f"ERROR: {str(e)[:20]}")
                
                file.write(" | ".join(row_data) + "\n")
            
            if count > 1000:
                file.write(f"\n... et {count - 1000} autres enregistrements (limite d'affichage atteinte)\n")
            
            file.write(f"\nTotal exporté : {min(count, 1000)} enregistrements\n\n")
            print(f"   ✅ {count} enregistrements exportés")
            
        except Exception as e:
            error_msg = f"Erreur lors de l'export de {model_name}: {str(e)}"
            file.write(f"\n{error_msg}\n\n")
            print(f"   ❌ Erreur: {error_msg}")

def export_database_schema():
    """Exporte le schéma de la base de données"""
    
    print("\n🔍 EXPORT DU SCHÉMA DE LA BASE DE DONNÉES")
    print("=" * 50)
    
    schema_file = f"export_database_schema_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(schema_file, 'w', encoding='utf-8') as f:
        f.write("SCHÉMA DE LA BASE DE DONNÉES\n")
        f.write("=" * 50 + "\n")
        f.write(f"Date d'export : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        with connection.cursor() as cursor:
            # Lister toutes les tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            f.write(f"TABLES TROUVÉES : {len(tables)}\n")
            f.write("-" * 30 + "\n")
            
            for table in tables:
                table_name = table[0]
                f.write(f"\nTABLE: {table_name}\n")
                f.write("-" * 20 + "\n")
                
                # Structure de la table
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()
                
                f.write("COLONNES:\n")
                for col in columns:
                    f.write(f"  - {col[1]} ({col[2]}) {'NOT NULL' if col[3] else 'NULL'}\n")
                
                # Compter les enregistrements
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                count = cursor.fetchone()[0]
                f.write(f"ENREGISTREMENTS: {count}\n")
    
    print(f"✅ Schéma exporté dans : {schema_file}")

if __name__ == "__main__":
    try:
        # Export principal
        exporter = ChatbotDatabaseExporter()
        exporter.export_all_data()
        
        # Export du schéma
        export_database_schema()
        
        print("\n🎉 EXPORT TERMINÉ AVEC SUCCÈS !")
        print("=" * 50)
        print("📁 Fichiers générés :")
        print(f"   • {exporter.output_file} (données complètes)")
        print(f"   • export_database_schema_*.txt (schéma)")
        print(f"📊 Total d'enregistrements : {exporter.total_records}")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de l'export : {e}")
        import traceback
        traceback.print_exc()
