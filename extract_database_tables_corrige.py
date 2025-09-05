#!/usr/bin/env python3
"""
Script corrigé pour extraire les tables et enregistrements utilisés par le chatbot ParcInfo
"""

import os
import sys
import django
from datetime import datetime

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()

def extract_users_table():
    """Extrait la table des utilisateurs"""
    print("📊 Extraction de la table des utilisateurs...")
    
    try:
        from apps.users.models import CustomUser
        
        users = CustomUser.objects.all().order_by('username')
        
        output = "=" * 80 + "\n"
        output += "TABLE : UTILISATEURS (CustomUser)\n"
        output += "=" * 80 + "\n\n"
        
        if users.exists():
            output += f"Total d'utilisateurs : {users.count()}\n\n"
            
            for user in users:
                output += f"👤 Utilisateur : {user.username}\n"
                output += f"   📧 Email : {user.email}\n"
                output += f"   📅 Date création : {user.date_joined.strftime('%Y-%m-%d %H:%M:%S')}\n"
                output += f"   ✅ Actif : {'Oui' if user.is_active else 'Non'}\n"
                output += f"   🔑 Super admin : {'Oui' if user.is_superuser else 'Non'}\n"
                output += f"   👥 Staff : {'Oui' if user.is_staff else 'Non'}\n"
                
                # Rôles et groupes
                groups = user.groups.all()
                if groups.exists():
                    output += f"   🎭 Groupes : {', '.join([g.name for g in groups])}\n"
                else:
                    output += f"   🎭 Groupes : (aucun groupe)\n"
                
                output += "\n" + "-" * 50 + "\n\n"
        else:
            output += "Aucun utilisateur trouvé.\n\n"
            
        return output
        
    except Exception as e:
        return f"❌ Erreur lors de l'extraction des utilisateurs : {e}\n\n"

def extract_suppliers_table():
    """Extrait la table des fournisseurs"""
    print("📊 Extraction de la table des fournisseurs...")
    
    try:
        from apps.fournisseurs.models import Fournisseur
        
        suppliers = Fournisseur.objects.all().order_by('nom')
        
        output = "=" * 80 + "\n"
        output += "TABLE : FOURNISSEURS (Fournisseur)\n"
        output += "=" * 80 + "\n\n"
        
        if suppliers.exists():
            output += f"Total de fournisseurs : {suppliers.count()}\n\n"
            
            for supplier in suppliers:
                output += f"🏢 Fournisseur : {supplier.nom}\n"
                output += f"   🆔 ICE : {supplier.ice}\n"
                output += f"   📍 Adresse : {supplier.adresse}\n"
                # Vérifier les champs disponibles
                if hasattr(supplier, 'telephone'):
                    output += f"   📞 Téléphone : {supplier.telephone or 'Non renseigné'}\n"
                if hasattr(supplier, 'email'):
                    output += f"   📧 Email : {supplier.email or 'Non renseigné'}\n"
                if hasattr(supplier, 'created_at'):
                    output += f"   📅 Date création : {supplier.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
                output += "\n" + "-" * 50 + "\n\n"
        else:
            output += "Aucun fournisseur trouvé.\n\n"
            
        return output
        
    except Exception as e:
        return f"❌ Erreur lors de l'extraction des fournisseurs : {e}\n\n"

def extract_bureau_materials_table():
    """Extrait la table des matériels bureautiques"""
    print("📊 Extraction de la table des matériels bureautiques...")
    
    try:
        from apps.materiel_bureautique.models import MaterielBureau
        
        materials = MaterielBureau.objects.all().order_by('code_inventaire')
        
        output = "=" * 80 + "\n"
        output += "TABLE : MATÉRIELS BUREAUTIQUES (MaterielBureau)\n"
        output += "=" * 80 + "\n\n"
        
        if materials.exists():
            output += f"Total de matériels bureautiques : {materials.count()}\n\n"
            
            for material in materials:
                # Gérer les propriétés qui peuvent retourner des chaînes ou des objets
                designation = getattr(material, 'designation', None)
                if designation:
                    if hasattr(designation, 'nom'):
                        designation_name = designation.nom
                    else:
                        designation_name = str(designation)
                else:
                    designation_name = 'Nom non renseigné'
                
                description = getattr(material, 'description', None)
                if description:
                    if hasattr(description, 'nom'):
                        description_name = description.nom
                    else:
                        description_name = str(description)
                else:
                    description_name = 'Description non renseignée'
                
                fournisseur = getattr(material, 'fournisseur', None)
                if fournisseur:
                    if hasattr(fournisseur, 'nom'):
                        fournisseur_name = fournisseur.nom
                    else:
                        fournisseur_name = str(fournisseur)
                else:
                    fournisseur_name = 'Fournisseur non renseigné'
                
                output += f"🪑 Matériel : {designation_name}\n"
                output += f"   🆔 Code inventaire : {material.code_inventaire}\n"
                output += f"   📝 Description : {description_name}\n"
                if hasattr(material, 'marque'):
                    output += f"   🏷️ Marque : {material.marque or 'Non renseigné'}\n"
                if hasattr(material, 'quantite'):
                    output += f"   📊 Quantité : {material.quantite}\n"
                if hasattr(material, 'prix_unitaire'):
                    output += f"   💰 Prix unitaire : {material.prix_unitaire or 'Non renseigné'}\n"
                if hasattr(material, 'localisation'):
                    output += f"   📍 Localisation : {material.localisation or 'Non renseigné'}\n"
                if hasattr(material, 'date_acquisition'):
                    output += f"   📅 Date acquisition : {material.date_acquisition.strftime('%Y-%m-%d') if material.date_acquisition else 'Non renseigné'}\n"
                output += f"   🏢 Fournisseur : {fournisseur_name}\n"
                if hasattr(material, 'utilisateur') and material.utilisateur:
                    output += f"   👤 Affecté à : {material.utilisateur.username}\n"
                if hasattr(material, 'statut'):
                    output += f"   📊 Statut : {material.statut}\n"
                if hasattr(material, 'lieu_stockage') and material.lieu_stockage:
                    output += f"   🏢 Lieu stockage : {material.lieu_stockage}\n"
                if hasattr(material, 'observation') and material.observation:
                    output += f"   📝 Observation : {material.observation}\n"
                output += "\n" + "-" * 50 + "\n\n"
        else:
            output += "Aucun matériel bureautique trouvé.\n\n"
            
        return output
        
    except Exception as e:
        return f"❌ Erreur lors de l'extraction des matériels bureautiques : {e}\n\n"

def extract_info_materials_table():
    """Extrait la table des matériels informatiques"""
    print("📊 Extraction de la table des matériels informatiques...")
    
    try:
        from apps.materiel_informatique.models import MaterielInformatique
        
        materials = MaterielInformatique.objects.all().order_by('code_inventaire')
        
        output = "=" * 80 + "\n"
        output += "TABLE : MATÉRIELS INFORMATIQUES (MaterielInformatique)\n"
        output += "=" * 80 + "\n\n"
        
        if materials.exists():
            output += f"Total de matériels informatiques : {materials.count()}\n\n"
            
            for material in materials:
                output += f"💻 Matériel : {getattr(material, 'designation', getattr(material, 'nom', 'Nom non renseigné'))}\n"
                output += f"   🆔 Code inventaire : {material.code_inventaire}\n"
                if hasattr(material, 'marque'):
                    output += f"   🏷️ Marque : {material.marque or 'Non renseigné'}\n"
                if hasattr(material, 'numero_serie'):
                    output += f"   🔢 Numéro série : {material.numero_serie or 'Non renseigné'}\n"
                if hasattr(material, 'quantite'):
                    output += f"   📊 Quantité : {material.quantite}\n"
                if hasattr(material, 'prix_unitaire'):
                    output += f"   💰 Prix unitaire : {material.prix_unitaire or 'Non renseigné'}\n"
                if hasattr(material, 'localisation'):
                    output += f"   📍 Localisation : {material.localisation or 'Non renseigné'}\n"
                if hasattr(material, 'date_acquisition'):
                    output += f"   📅 Date acquisition : {material.date_acquisition.strftime('%Y-%m-%d') if material.date_acquisition else 'Non renseigné'}\n"
                if hasattr(material, 'fournisseur') and material.fournisseur:
                    output += f"   🏢 Fournisseur : {material.fournisseur.nom}\n"
                if hasattr(material, 'utilisateur') and material.utilisateur:
                    output += f"   👤 Affecté à : {material.utilisateur.username}\n"
                if hasattr(material, 'statut'):
                    output += f"   📊 Statut : {material.statut}\n"
                output += "\n" + "-" * 50 + "\n\n"
        else:
            output += "Aucun matériel informatique trouvé.\n\n"
            
        return output
        
    except Exception as e:
        return f"❌ Erreur lors de l'extraction des matériels informatiques : {e}\n\n"

def extract_info_orders_table():
    """Extrait la table des commandes informatiques"""
    print("📊 Extraction de la table des commandes informatiques...")
    
    try:
        from apps.commande_informatique.models import Commande
        
        orders = Commande.objects.all().order_by('numero_commande')
        
        output = "=" * 80 + "\n"
        output += "TABLE : COMMANDES INFORMATIQUES (Commande)\n"
        output += "=" * 80 + "\n\n"
        
        if orders.exists():
            output += f"Total de commandes informatiques : {orders.count()}\n\n"
            
            for order in orders:
                output += f"📦 Commande : {order.numero_commande}\n"
                if hasattr(order, 'date_commande'):
                    output += f"   📅 Date commande : {order.date_commande.strftime('%Y-%m-%d')}\n"
                if hasattr(order, 'date_reception'):
                    output += f"   📅 Date réception : {order.date_reception.strftime('%Y-%m-%d') if order.date_reception else 'Non reçue'}\n"
                if hasattr(order, 'mode_passation'):
                    output += f"   📋 Mode passation : {order.mode_passation}\n"
                if hasattr(order, 'numero_facture'):
                    output += f"   🧾 Numéro facture : {order.numero_facture or 'Non renseigné'}\n"
                if hasattr(order, 'duree_garantie_valeur') and hasattr(order, 'duree_garantie_unite'):
                    output += f"   ⏰ Durée garantie : {order.duree_garantie_valeur} {order.duree_garantie_unite}\n"
                if hasattr(order, 'fournisseur') and order.fournisseur:
                    output += f"   🏢 Fournisseur : {order.fournisseur.nom}\n"
                if hasattr(order, 'montant_total'):
                    output += f"   💰 Montant total : {order.montant_total}\n"
                output += "\n" + "-" * 50 + "\n\n"
        else:
            output += "Aucune commande informatique trouvée.\n\n"
            
        return output
        
    except Exception as e:
        return f"❌ Erreur lors de l'extraction des commandes informatiques : {e}\n\n"

def extract_info_order_lines_table():
    """Extrait la table des lignes de commande informatiques"""
    print("📊 Extraction de la table des lignes de commande informatiques...")
    
    try:
        from apps.commande_informatique.models import LigneCommande, Designation, Description
        
        lines = LigneCommande.objects.all().order_by('id')
        
        output = "=" * 80 + "\n"
        output += "TABLE : LIGNES DE COMMANDE INFORMATIQUES (LigneCommande)\n"
        output += "=" * 80 + "\n\n"
        
        if lines.exists():
            output += f"Total de lignes de commande : {lines.count()}\n\n"
            
            for line in lines:
                output += f"📋 Ligne : {line.id}\n"
                if hasattr(line, 'commande') and line.commande:
                    output += f"   📦 Commande : {line.commande.numero_commande}\n"
                if hasattr(line, 'designation') and line.designation:
                    output += f"   🏷️ Désignation : {line.designation.nom}\n"
                if hasattr(line, 'description') and line.description:
                    output += f"   📝 Description : {line.description.nom}\n"
                if hasattr(line, 'quantite'):
                    output += f"   📊 Quantité : {line.quantite}\n"
                if hasattr(line, 'prix_unitaire'):
                    output += f"   💰 Prix unitaire : {line.prix_unitaire}\n"
                output += "\n" + "-" * 50 + "\n\n"
        else:
            output += "Aucune ligne de commande informatique trouvée.\n\n"
            
        return output
        
    except Exception as e:
        return f"❌ Erreur lors de l'extraction des lignes de commande informatiques : {e}\n\n"

def extract_designations_table():
    """Extrait la table des désignations"""
    print("📊 Extraction de la table des désignations...")
    
    try:
        from apps.commande_informatique.models import Designation
        
        designations = Designation.objects.all().order_by('nom')
        
        output = "=" * 80 + "\n"
        output += "TABLE : DÉSIGNATIONS (Designation)\n"
        output += "=" * 80 + "\n\n"
        
        if designations.exists():
            output += f"Total de désignations : {designations.count()}\n\n"
            
            for designation in designations:
                output += f"🏷️ Désignation : {designation.nom}\n"
                output += "\n" + "-" * 50 + "\n\n"
        else:
            output += "Aucune désignation trouvée.\n\n"
            
        return output
        
    except Exception as e:
        return f"❌ Erreur lors de l'extraction des désignations : {e}\n\n"

def extract_descriptions_table():
    """Extrait la table des descriptions"""
    print("📊 Extraction de la table des descriptions...")
    
    try:
        from apps.commande_informatique.models import Description
        
        descriptions = Description.objects.all().order_by('nom')
        
        output = "=" * 80 + "\n"
        output += "TABLE : DESCRIPTIONS (Description)\n"
        output += "=" * 80 + "\n\n"
        
        if descriptions.exists():
            output += f"Total de descriptions : {descriptions.count()}\n\n"
            
            for description in descriptions:
                output += f"📝 Description : {description.nom}\n"
                if hasattr(description, 'designation') and description.designation:
                    output += f"   🏷️ Désignation : {description.designation.nom}\n"
                output += "\n" + "-" * 50 + "\n\n"
        else:
            output += "Aucune description trouvée.\n\n"
            
        return output
        
    except Exception as e:
        return f"❌ Erreur lors de l'extraction des descriptions : {e}\n\n"

def extract_bureau_orders_table():
    """Extrait la table des commandes bureautiques"""
    print("📊 Extraction de la table des commandes bureautiques...")
    
    try:
        from apps.commande_bureau.models import CommandeBureau
        
        orders = CommandeBureau.objects.all().order_by('numero_commande')
        
        output = "=" * 80 + "\n"
        output += "TABLE : COMMANDES BUREAUTIQUES (CommandeBureau)\n"
        output += "=" * 80 + "\n\n"
        
        if orders.exists():
            output += f"Total de commandes bureautiques : {orders.count()}\n\n"
            
            for order in orders:
                output += f"📦 Commande : {order.numero_commande}\n"
                if hasattr(order, 'date_commande'):
                    output += f"   📅 Date commande : {order.date_commande.strftime('%Y-%m-%d')}\n"
                if hasattr(order, 'date_reception'):
                    output += f"   📅 Date réception : {order.date_reception.strftime('%Y-%m-%d') if order.date_reception else 'Non reçue'}\n"
                if hasattr(order, 'fournisseur') and order.fournisseur:
                    output += f"   🏢 Fournisseur : {order.fournisseur.nom}\n"
                if hasattr(order, 'montant_total'):
                    output += f"   💰 Montant total : {order.montant_total or 'Non renseigné'}\n"
                if hasattr(order, 'numero_facture'):
                    output += f"   📄 Numéro facture : {order.numero_facture or 'Non renseigné'}\n"
                if hasattr(order, 'statut'):
                    output += f"   📊 Statut : {order.statut}\n"
                if hasattr(order, 'duree_garantie'):
                    output += f"   📅 Durée garantie : {order.duree_garantie or 'Non renseigné'}\n"
                if hasattr(order, 'observations'):
                    output += f"   📝 Observations : {order.observations or 'Aucune'}\n"
                output += "\n" + "-" * 50 + "\n\n"
        else:
            output += "Aucune commande bureautique trouvée.\n\n"
            
        return output
        
    except Exception as e:
        return f"❌ Erreur lors de l'extraction des commandes bureautiques : {e}\n\n"

def extract_deliveries_table():
    """Extrait la table des livraisons"""
    print("📊 Extraction de la table des livraisons...")
    
    try:
        from apps.livraison.models import Livraison
        
        deliveries = Livraison.objects.all().order_by('id')
        
        output = "=" * 80 + "\n"
        output += "TABLE : LIVRAISONS (Livraison)\n"
        output += "=" * 80 + "\n\n"
        
        if deliveries.exists():
            output += f"Total de livraisons : {deliveries.count()}\n\n"
            
            for delivery in deliveries:
                output += f"🚚 Livraison : {delivery.id}\n"
                if hasattr(delivery, 'numero_commande'):
                    output += f"   📦 Commande : {delivery.numero_commande}\n"
                if hasattr(delivery, 'date_livraison_prevue'):
                    output += f"   📅 Date prévue : {delivery.date_livraison_prevue.strftime('%Y-%m-%d') if delivery.date_livraison_prevue else 'Non renseigné'}\n"
                if hasattr(delivery, 'date_livraison_effective'):
                    output += f"   📅 Date effective : {delivery.date_livraison_effective.strftime('%Y-%m-%d') if delivery.date_livraison_effective else 'Non livrée'}\n"
                if hasattr(delivery, 'statut_livraison'):
                    output += f"   📊 Statut : {delivery.statut_livraison}\n"
                if hasattr(delivery, 'notes'):
                    output += f"   📝 Notes : {delivery.notes or 'Aucune'}\n"
                if hasattr(delivery, 'cree_par') and delivery.cree_par:
                    output += f"   👤 Créé par : {delivery.cree_par.username}\n"
                output += "\n" + "-" * 50 + "\n\n"
        else:
            output += "Aucune livraison trouvée.\n\n"
            
        return output
        
    except Exception as e:
        return f"❌ Erreur lors de l'extraction des livraisons : {e}\n\n"

def extract_equipment_requests_table():
    """Extrait la table des demandes d'équipement"""
    print("📊 Extraction de la table des demandes d'équipement...")
    
    try:
        from apps.demande_equipement.models import DemandeEquipement
        
        requests = DemandeEquipement.objects.all().order_by('date_demande')
        
        output = "=" * 80 + "\n"
        output += "TABLE : DEMANDES D'ÉQUIPEMENT (DemandeEquipement)\n"
        output += "=" * 80 + "\n\n"
        
        if requests.exists():
            output += f"Total de demandes d'équipement : {requests.count()}\n\n"
            
            for request in requests:
                output += f"📋 Demande : {request.id}\n"
                if hasattr(request, 'demandeur') and request.demandeur:
                    output += f"   👤 Demandeur : {request.demandeur.username}\n"
                if hasattr(request, 'date_demande'):
                    output += f"   📅 Date demande : {request.date_demande.strftime('%Y-%m-%d')}\n"
                if hasattr(request, 'date_approbation'):
                    output += f"   📅 Date approbation : {request.date_approbation.strftime('%Y-%m-%d') if request.date_approbation else 'Non approuvée'}\n"
                if hasattr(request, 'statut'):
                    output += f"   📊 Statut : {request.statut}\n"
                if hasattr(request, 'description'):
                    output += f"   📝 Description : {request.description or 'Aucune'}\n"
                if hasattr(request, 'type_equipement'):
                    output += f"   🏷️ Type équipement : {request.type_equipement or 'Non renseigné'}\n"
                if hasattr(request, 'priorite'):
                    output += f"   📊 Priorité : {request.priorite}\n"
                if hasattr(request, 'approuve_par') and request.approuve_par:
                    output += f"   👤 Approuvé par : {request.approuve_par.username}\n"
                output += "\n" + "-" * 50 + "\n\n"
        else:
            output += "Aucune demande d'équipement trouvée.\n\n"
            
        return output
        
    except Exception as e:
        return f"❌ Erreur lors de l'extraction des demandes d'équipement : {e}\n\n"

def extract_chatbot_interactions():
    """Extrait la table des interactions du chatbot"""
    print("📊 Extraction de la table des interactions du chatbot...")
    
    try:
        from apps.chatbot.models import ChatbotInteraction
        
        interactions = ChatbotInteraction.objects.all().order_by('-timestamp')[:100]  # 100 dernières
        
        output = "=" * 80 + "\n"
        output += "TABLE : INTERACTIONS DU CHATBOT (ChatbotInteraction)\n"
        output += "=" * 80 + "\n\n"
        
        if interactions.exists():
            output += f"Total d'interactions (100 dernières affichées) : {ChatbotInteraction.objects.count()}\n\n"
            
            for interaction in interactions:
                output += f"💬 Interaction : {interaction.id}\n"
                if hasattr(interaction, 'user') and interaction.user:
                    output += f"   👤 Utilisateur : {interaction.user.username}\n"
                else:
                    output += f"   👤 Utilisateur : Anonyme\n"
                output += f"   📅 Date : {interaction.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
                output += f"   ❓ Question : {interaction.query[:100]}{'...' if len(interaction.query) > 100 else ''}\n"
                output += f"   💡 Réponse : {interaction.response[:100]}{'...' if len(interaction.response) > 100 else ''}\n"
                if hasattr(interaction, 'intent'):
                    output += f"   🎯 Intent : {interaction.intent or 'Non détecté'}\n"
                if hasattr(interaction, 'confidence'):
                    output += f"   📊 Confidence : {interaction.confidence or 'Non renseigné'}\n"
                if hasattr(interaction, 'source'):
                    output += f"   🔍 Source : {interaction.source or 'Non renseigné'}\n"
                output += "\n" + "-" * 50 + "\n\n"
        else:
            output += "Aucune interaction du chatbot trouvée.\n\n"
            
        return output
        
    except Exception as e:
        return f"❌ Erreur lors de l'extraction des interactions du chatbot : {e}\n\n"

def main():
    """Fonction principale d'extraction"""
    print("🚀 EXTRACTION DES TABLES ET ENREGISTREMENTS DE LA BASE DE DONNÉES")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Créer le contenu du fichier
    content = ""
    content += "📊 EXTRACTION COMPLÈTE DE LA BASE DE DONNÉES PARCINFO\n"
    content += f"📅 Date d'extraction : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    content += "🎯 Tables utilisées par le chatbot ParcInfo\n"
    content += "=" * 80 + "\n\n"
    
    # Extraire chaque table
    content += extract_users_table()
    content += extract_suppliers_table()
    content += extract_bureau_materials_table()
    content += extract_info_materials_table()
    content += extract_info_orders_table()
    content += extract_info_order_lines_table()
    content += extract_designations_table()
    content += extract_descriptions_table()
    content += extract_bureau_orders_table()
    content += extract_deliveries_table()
    content += extract_equipment_requests_table()
    content += extract_chatbot_interactions()
    
    # Ajouter un résumé
    content += "=" * 80 + "\n"
    content += "📊 RÉSUMÉ DE L'EXTRACTION\n"
    content += "=" * 80 + "\n\n"
    content += "✅ Extraction terminée avec succès !\n"
    content += f"📅 Fichier généré le : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    content += "🎯 Toutes les tables utilisées par le chatbot ont été extraites.\n"
    content += "📁 Le fichier contient la structure complète de la base de données.\n\n"
    
    # Sauvegarder dans un fichier
    filename = f"database_extraction_corrige_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n✅ Extraction terminée avec succès !")
        print(f"📁 Fichier sauvegardé : {filename}")
        print(f"📊 Toutes les tables ont été extraites et sauvegardées.")
        
        # Afficher un aperçu
        print(f"\n📄 Aperçu du contenu (premières lignes) :")
        print("-" * 50)
        lines = content.split('\n')[:20]
        for line in lines:
            print(line)
        print("...")
        
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde : {e}")

if __name__ == "__main__":
    main()
