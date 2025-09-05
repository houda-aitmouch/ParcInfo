#!/usr/bin/env python3
"""
Script d'export final de la base de données des modèles utilisés par le chatbot
Version finale avec tous les champs corrects
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
    """Exportateur final de la base de données pour le chatbot"""
    
    def __init__(self):
        self.output_file = f"export_chatbot_database_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        self.total_records = 0
        
    def export_all_data(self):
        """Exporte toutes les données des modèles utilisés par le chatbot"""
        
        print("🚀 EXPORT FINAL DE LA BASE DE DONNÉES CHATBOT")
        print("=" * 80)
        print(f"📅 Date d'export : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 Fichier de sortie : {self.output_file}")
        print()
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            # En-tête du fichier
            f.write("=" * 80 + "\n")
            f.write("EXPORT FINAL DE LA BASE DE DONNÉES - MODÈLES CHATBOT\n")
            f.write("=" * 80 + "\n")
            f.write(f"Date d'export : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Généré par : Script d'export final (tous champs corrects)\n")
            f.write("=" * 80 + "\n\n")
            
            # Export de chaque modèle avec les bons champs
            models_to_export = [
                ("UTILISATEURS", CustomUser, [
                    'id', 'username', 'email', 'first_name', 'last_name', 
                    'is_active', 'is_staff', 'is_superuser', 'date_joined'
                ]),
                ("GROUPES", Group, ['id', 'name']),
                ("FOURNISSEURS", Fournisseur, [
                    'id', 'nom', 'adresse', 'telephone', 'email', 'contact_principal'
                ]),
                ("DESIGNATIONS INFORMATIQUE", Designation, ['id', 'nom']),
                ("DESCRIPTIONS INFORMATIQUE", Description, ['id', 'nom']),
                ("COMMANDES INFORMATIQUE", Commande, [
                    'id', 'numero_commande', 'date_commande', 'montant_total', 'statut'
                ]),
                ("LIGNES COMMANDE INFORMATIQUE", LigneCommande, [
                    'id', 'quantite', 'prix_unitaire', 'montant_total'
                ]),
                ("MATÉRIELS INFORMATIQUE", MaterielInformatique, [
                    'id', 'code_inventaire', 'numero_serie', 'statut', 'date_affectation'
                ]),
                ("DESIGNATIONS BUREAUTIQUE", DesignationBureau, ['id', 'nom']),
                ("DESCRIPTIONS BUREAUTIQUE", DescriptionBureau, ['id', 'nom']),
                ("COMMANDES BUREAUTIQUE", CommandeBureau, [
                    'id', 'numero_commande', 'date_commande', 'montant_total', 'statut'
                ]),
                ("LIGNES COMMANDE BUREAUTIQUE", LigneCommandeBureau, [
                    'id', 'quantite', 'prix_unitaire', 'montant_total'
                ]),
                ("MATÉRIELS BUREAUTIQUE", MaterielBureau, [
                    'id', 'code_inventaire', 'statut', 'date_affectation'
                ]),
                ("LIVRAISONS", Livraison, [
                    'id', 'numero_livraison', 'date_livraison', 'statut', 'commentaires'
                ]),
                ("DEMANDES D'ÉQUIPEMENT", DemandeEquipement, [
                    'id', 'categorie', 'type_article', 'type_demande', 'statut', 'date_demande'
                ]),
                ("FOURNITURES", Fourniture, [
                    'id', 'quantite', 'prix_unitaire'
                ]),
                ("ARCHIVES DÉCHARGE", ArchiveDecharge, [
                    'id', 'date_signature', 'statut'
                ]),
                ("EXEMPLES D'INTENTIONS CHATBOT", IntentExample, [
                    'id', 'intent', 'phrase', 'weight', 'source', 'created_at'
                ]),
                ("FEEDBACK CHATBOT", ChatbotFeedback, [
                    'id', 'rating', 'comment', 'created_at'
                ]),
                ("INTERACTIONS CHATBOT", ChatbotInteraction, [
                    'id', 'session_id', 'user_query', 'detected_intent', 'sql_attempted', 
                    'sql_results', 'rag_results', 'final_response', 'timestamp'
                ])
            ]
            
            for model_name, model_class, fields in models_to_export:
                self._export_model(f, model_name, model_class, fields)
            
            # Statistiques finales
            f.write("\n" + "=" * 80 + "\n")
            f.write("STATISTIQUES D'EXPORT FINAL\n")
            f.write("=" * 80 + "\n")
            f.write(f"Total d'enregistrements exportés : {self.total_records}\n")
            f.write(f"Date de fin d'export : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n")
        
        print(f"✅ Export final terminé avec succès !")
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
            limit = 1000 if model_name != "INTERACTIONS CHATBOT" else 500
            exported_count = 0
            
            for obj in model_class.objects.all()[:limit]:
                row_data = []
                for field in fields:
                    try:
                        value = getattr(obj, field)
                        
                        # Gestion des différents types de données
                        if value is None:
                            value = "NULL"
                        elif hasattr(value, 'pk'):  # ForeignKey
                            value = f"{value.__class__.__name__}(id={value.pk})"
                        elif hasattr(value, 'all'):  # ManyToManyField
                            related_objects = list(value.all()[:2])  # Limite à 2
                            value = f"[{', '.join([f'{obj.__class__.__name__}(id={obj.pk})' for obj in related_objects])}]"
                        elif isinstance(value, datetime):
                            value = value.strftime('%Y-%m-%d %H:%M:%S')
                        elif isinstance(value, (int, float)):
                            value = str(value)
                        elif isinstance(value, bool):
                            value = str(value)
                        else:
                            value = str(value)
                        
                        # Limiter la longueur pour la lisibilité
                        if len(value) > 80:
                            value = value[:77] + "..."
                        
                        row_data.append(value)
                        
                    except Exception as e:
                        row_data.append(f"ERROR: {str(e)[:20]}")
                
                file.write(" | ".join(row_data) + "\n")
                exported_count += 1
            
            if count > limit:
                file.write(f"\n... et {count - limit} autres enregistrements (limite d'affichage atteinte)\n")
            
            file.write(f"\nTotal exporté : {exported_count} enregistrements\n\n")
            print(f"   ✅ {exported_count} enregistrements exportés (sur {count} total)")
            
        except Exception as e:
            error_msg = f"Erreur lors de l'export de {model_name}: {str(e)}"
            file.write(f"\n{error_msg}\n\n")
            print(f"   ❌ Erreur: {error_msg}")

def export_summary():
    """Exporte un résumé des données exportées"""
    
    print("\n📊 GÉNÉRATION DU RÉSUMÉ")
    print("=" * 40)
    
    summary_file = f"resume_export_chatbot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("RÉSUMÉ DE L'EXPORT DE LA BASE DE DONNÉES CHATBOT\n")
        f.write("=" * 60 + "\n")
        f.write(f"Date d'export : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("MODÈLES EXPORTÉS :\n")
        f.write("-" * 20 + "\n")
        
        models_info = [
            ("Utilisateurs", CustomUser, "Utilisateurs du système"),
            ("Groupes", Group, "Groupes de permissions"),
            ("Fournisseurs", Fournisseur, "Fournisseurs de matériel"),
            ("Designations Informatique", Designation, "Désignations matériel informatique"),
            ("Descriptions Informatique", Description, "Descriptions matériel informatique"),
            ("Commandes Informatique", Commande, "Commandes de matériel informatique"),
            ("Lignes Commande Informatique", LigneCommande, "Lignes de commande informatique"),
            ("Matériels Informatique", MaterielInformatique, "Matériels informatiques"),
            ("Designations Bureautique", DesignationBureau, "Désignations matériel bureautique"),
            ("Descriptions Bureautique", DescriptionBureau, "Descriptions matériel bureautique"),
            ("Commandes Bureautique", CommandeBureau, "Commandes de matériel bureautique"),
            ("Lignes Commande Bureautique", LigneCommandeBureau, "Lignes de commande bureautique"),
            ("Matériels Bureautique", MaterielBureau, "Matériels bureautiques"),
            ("Livraisons", Livraison, "Livraisons de matériel"),
            ("Demandes d'équipement", DemandeEquipement, "Demandes d'équipement"),
            ("Fournitures", Fourniture, "Fournitures des demandes"),
            ("Archives Décharge", ArchiveDecharge, "Archives des décharges"),
            ("Exemples Intentions Chatbot", IntentExample, "Exemples d'intentions pour le chatbot"),
            ("Feedback Chatbot", ChatbotFeedback, "Retours utilisateurs sur le chatbot"),
            ("Interactions Chatbot", ChatbotInteraction, "Interactions avec le chatbot")
        ]
        
        total_records = 0
        for name, model, description in models_info:
            try:
                count = model.objects.count()
                total_records += count
                f.write(f"{name:30} : {count:>6} enregistrements - {description}\n")
            except Exception as e:
                f.write(f"{name:30} : ERREUR - {str(e)}\n")
        
        f.write("-" * 60 + "\n")
        f.write(f"{'TOTAL':30} : {total_records:>6} enregistrements\n\n")
        
        f.write("UTILISATION :\n")
        f.write("-" * 10 + "\n")
        f.write("Ce fichier contient un export complet de tous les modèles\n")
        f.write("utilisés par le système de chatbot ParcInfo.\n")
        f.write("Les données sont formatées en colonnes séparées par '|'.\n")
        f.write("Chaque section commence par les métadonnées du modèle.\n\n")
        
        f.write("FICHIERS GÉNÉRÉS :\n")
        f.write("-" * 15 + "\n")
        f.write("• export_chatbot_database_final_*.txt : Données complètes\n")
        f.write("• resume_export_chatbot_*.txt : Ce résumé\n")
    
    print(f"✅ Résumé généré : {summary_file}")

if __name__ == "__main__":
    try:
        # Export principal
        exporter = ChatbotDatabaseExporter()
        exporter.export_all_data()
        
        # Export du résumé
        export_summary()
        
        print("\n🎉 EXPORT FINAL TERMINÉ AVEC SUCCÈS !")
        print("=" * 60)
        print("📁 Fichiers générés :")
        print(f"   • {exporter.output_file} (données complètes)")
        print(f"   • resume_export_chatbot_*.txt (résumé)")
        print(f"📊 Total d'enregistrements : {exporter.total_records}")
        print("\n✅ L'export complet de la base de données chatbot est prêt !")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de l'export : {e}")
        import traceback
        traceback.print_exc()
