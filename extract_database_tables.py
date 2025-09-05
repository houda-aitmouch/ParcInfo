#!/usr/bin/env python3
"""
Script pour extraire les tables et enregistrements utilisés par le chatbot ParcInfo
"""

import os
import sys
import django
from datetime import datetime
import json

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
                output += f"   📞 Téléphone : {supplier.telephone or 'Non renseigné'}\n"
                output += f"   📧 Email : {supplier.email or 'Non renseigné'}\n"
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
        from apps.materiel_bureautique.models import MaterielBureautique
        
        materials = MaterielBureautique.objects.all().order_by('code_inventaire')
        
        output = "=" * 80 + "\n"
        output += "TABLE : MATÉRIELS BUREAUTIQUES (MaterielBureautique)\n"
        output += "=" * 80 + "\n\n"
        
        if materials.exists():
            output += f"Total de matériels bureautiques : {materials.count()}\n\n"
            
            for material in materials:
                output += f"🪑 Matériel : {material.designation}\n"
                output += f"   🆔 Code inventaire : {material.code_inventaire}\n"
                output += f"   🏷️ Marque : {material.marque or 'Non renseigné'}\n"
                output += f"   📊 Quantité : {material.quantite}\n"
                output += f"   💰 Prix unitaire : {material.prix_unitaire or 'Non renseigné'}\n"
                output += f"   📍 Localisation : {material.localisation or 'Non renseigné'}\n"
                output += f"   📅 Date acquisition : {material.date_acquisition.strftime('%Y-%m-%d') if material.date_acquisition else 'Non renseigné'}\n"
                output += f"   🏢 Fournisseur : {material.fournisseur.nom if material.fournisseur else 'Non renseigné'}\n"
                output += f"   👤 Affecté à : {material.utilisateur.username if material.utilisateur else 'Non affecté'}\n"
                output += f"   📊 Statut : {material.get_statut_display()}\n"
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
                output += f"💻 Matériel : {material.designation}\n"
                output += f"   🆔 Code inventaire : {material.code_inventaire}\n"
                output += f"   🏷️ Marque : {material.marque or 'Non renseigné'}\n"
                output += f"   🔢 Numéro série : {material.numero_serie or 'Non renseigné'}\n"
                output += f"   📊 Quantité : {material.quantite}\n"
                output += f"   💰 Prix unitaire : {material.prix_unitaire or 'Non renseigné'}\n"
                output += f"   📍 Localisation : {material.localisation or 'Non renseigné'}\n"
                output += f"   📅 Date acquisition : {material.date_acquisition.strftime('%Y-%m-%d') if material.date_acquisition else 'Non renseigné'}\n"
                output += f"   🏢 Fournisseur : {material.fournisseur.nom if material.fournisseur else 'Non renseigné'}\n"
                output += f"   👤 Affecté à : {material.utilisateur.username if material.utilisateur else 'Non affecté'}\n"
                output += f"   📊 Statut : {material.get_statut_display()}\n"
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
        from apps.commande_informatique.models import CommandeInformatique
        
        orders = CommandeInformatique.objects.all().order_by('numero_commande')
        
        output = "=" * 80 + "\n"
        output += "TABLE : COMMANDES INFORMATIQUES (CommandeInformatique)\n"
        output += "=" * 80 + "\n\n"
        
        if orders.exists():
            output += f"Total de commandes informatiques : {orders.count()}\n\n"
            
            for order in orders:
                output += f"📦 Commande : {order.numero_commande}\n"
                output += f"   📅 Date commande : {order.date_commande.strftime('%Y-%m-%d')}\n"
                output += f"   📅 Date réception : {order.date_reception.strftime('%Y-%m-%d') if order.date_reception else 'Non reçue'}\n"
                output += f"   🏢 Fournisseur : {order.fournisseur.nom if order.fournisseur else 'Non renseigné'}\n"
                output += f"   💰 Montant total : {order.montant_total or 'Non renseigné'}\n"
                output += f"   📄 Numéro facture : {order.numero_facture or 'Non renseigné'}\n"
                output += f"   📊 Statut : {order.get_statut_display()}\n"
                output += f"   📅 Durée garantie : {order.duree_garantie or 'Non renseigné'}\n"
                output += f"   📝 Observations : {order.observations or 'Aucune'}\n"
                output += "\n" + "-" * 50 + "\n\n"
        else:
            output += "Aucune commande informatique trouvée.\n\n"
            
        return output
        
    except Exception as e:
        return f"❌ Erreur lors de l'extraction des commandes informatiques : {e}\n\n"

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
                output += f"   📅 Date commande : {order.date_commande.strftime('%Y-%m-%d')}\n"
                output += f"   📅 Date réception : {order.date_reception.strftime('%Y-%m-%d') if order.date_reception else 'Non reçue'}\n"
                output += f"   🏢 Fournisseur : {order.fournisseur.nom if order.fournisseur else 'Non renseigné'}\n"
                output += f"   💰 Montant total : {order.montant_total or 'Non renseigné'}\n"
                output += f"   📄 Numéro facture : {order.numero_facture or 'Non renseigné'}\n"
                output += f"   📊 Statut : {order.get_statut_display()}\n"
                output += f"   📅 Durée garantie : {order.duree_garantie or 'Non renseigné'}\n"
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
        
        deliveries = Livraison.objects.all().order_by('numero_livraison')
        
        output = "=" * 80 + "\n"
        output += "TABLE : LIVRAISONS (Livraison)\n"
        output += "=" * 80 + "\n\n"
        
        if deliveries.exists():
            output += f"Total de livraisons : {deliveries.count()}\n\n"
            
            for delivery in deliveries:
                output += f"🚚 Livraison : {delivery.numero_livraison}\n"
                output += f"   📦 Commande : {delivery.commande.numero_commande if delivery.commande else 'Non renseigné'}\n"
                output += f"   📅 Date prévue : {delivery.date_prevue.strftime('%Y-%m-%d') if delivery.date_prevue else 'Non renseigné'}\n"
                output += f"   📅 Date effective : {delivery.date_effective.strftime('%Y-%m-%d') if delivery.date_effective else 'Non livrée'}\n"
                output += f"   📊 Statut : {delivery.get_statut_display()}\n"
                output += f"   📝 Observations : {delivery.observations or 'Aucune'}\n"
                output += f"   👤 Responsable : {delivery.responsable.username if delivery.responsable else 'Non renseigné'}\n"
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
                output += f"   👤 Demandeur : {request.demandeur.username if request.demandeur else 'Non renseigné'}\n"
                output += f"   📅 Date demande : {request.date_demande.strftime('%Y-%m-%d')}\n"
                output += f"   📅 Date approbation : {request.date_approbation.strftime('%Y-%m-%d') if request.date_approbation else 'Non approuvée'}\n"
                output += f"   📊 Statut : {request.get_statut_display()}\n"
                output += f"   📝 Description : {request.description or 'Aucune'}\n"
                output += f"   🏷️ Type équipement : {request.type_equipement or 'Non renseigné'}\n"
                output += f"   📊 Priorité : {request.get_priorite_display()}\n"
                output += f"   👤 Approuvé par : {request.approuve_par.username if request.approuve_par else 'Non approuvé'}\n"
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
                output += f"   👤 Utilisateur : {interaction.user.username if interaction.user else 'Anonyme'}\n"
                output += f"   📅 Date : {interaction.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
                output += f"   ❓ Question : {interaction.query[:100]}{'...' if len(interaction.query) > 100 else ''}\n"
                output += f"   💡 Réponse : {interaction.response[:100]}{'...' if len(interaction.response) > 100 else ''}\n"
                output += f"   🎯 Intent : {interaction.intent or 'Non détecté'}\n"
                output += f"   📊 Confidence : {interaction.confidence or 'Non renseigné'}\n"
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
    filename = f"database_extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
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
