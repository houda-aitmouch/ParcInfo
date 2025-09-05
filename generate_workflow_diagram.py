#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de Diagramme de Workflow ParcInfo
============================================

Ce script génère un diagramme de workflow visuel pour le système ParcInfo
basé sur le workflow manuel documenté.

Auteur: Équipe ParcInfo
Date: 2025-01-15
"""

from graphviz import Digraph
import os
import sys

def create_workflow_diagram():
    """Crée le diagramme de workflow ParcInfo complet."""
    
    # Création du graphe principal
    dot = Digraph('Workflow_ParcInfo_Complet', format='png')
    dot.attr(rankdir='TB', size='16,12', dpi='300')
    dot.attr('node', fontname='Arial', fontsize='10')
    dot.attr('edge', fontname='Arial', fontsize='9')
    
    # Définition des couleurs par rôle
    roles_colors = {
        'Employé': '#E3F2FD',           # Bleu clair
        'Secrétaire': '#F3E5F5',        # Violet clair
        'Gestionnaire_Info': '#E8F5E8',  # Vert clair
        'Gestionnaire_Bureau': '#FFF3E0', # Orange clair
        'SuperAdmin': '#F1F8E9',        # Vert très clair
        'Système': '#FFEBEE',           # Rouge très clair
        'Décision': '#FFFFFF',          # Blanc pour les décisions
        'Début_Fin': '#E0E0E0'          # Gris pour début/fin
    }
    
    # Styles des nœuds
    node_styles = {
        'process': {'shape': 'box', 'style': 'filled,rounded'},
        'decision': {'shape': 'diamond', 'style': 'filled'},
        'start_end': {'shape': 'circle', 'style': 'filled'},
        'document': {'shape': 'note', 'style': 'filled'}
    }
    
    # === NŒUDS DE DÉBUT ET FIN ===
    dot.node('Start', 'DÉBUT\nDemande d\'équipement', 
             **node_styles['start_end'], fillcolor=roles_colors['Début_Fin'])
    dot.node('End_Approuve', 'FIN\nDemande approuvée', 
             **node_styles['start_end'], fillcolor=roles_colors['Début_Fin'])
    dot.node('End_Refuse', 'FIN\nDemande refusée', 
             **node_styles['start_end'], fillcolor=roles_colors['Début_Fin'])
    
    # === WORKFLOW 1: DEMANDE D'ÉQUIPEMENT ===
    
    # Étape 1: Création de la demande
    dot.node('Demande', '1. Créer demande d\'équipement\n(Formulaire papier)', 
             **node_styles['process'], fillcolor=roles_colors['Employé'])
    
    # Étape 2: Enregistrement
    dot.node('Enregistrement', '2. Enregistrement et classement\n(Numéro D-YYYY-XXX)', 
             **node_styles['process'], fillcolor=roles_colors['Secrétaire'])
    
    # Étape 3: Vérification stock
    dot.node('Stock', '3. Vérifier stock disponible\n(Registre d\'inventaire)', 
             **node_styles['process'], fillcolor=roles_colors['Gestionnaire_Info'])
    
    # Décision stock
    dot.node('StockCheck', 'Stock suffisant ?', 
             **node_styles['decision'], fillcolor=roles_colors['Décision'])
    
    # Étape 4: Analyse
    dot.node('Analyse', '4. Analyser demande\n(Budget + justification)', 
             **node_styles['process'], fillcolor=roles_colors['Gestionnaire_Info'])
    
    # Décision approbation
    dot.node('Approval', 'Demande approuvée ?', 
             **node_styles['decision'], fillcolor=roles_colors['Décision'])
    
    # Notification refus
    dot.node('Notification_Refus', '5. Notification de refus\n(Courrier interne)', 
             **node_styles['process'], fillcolor=roles_colors['Secrétaire'])
    
    # === WORKFLOW 2: AFFECTATION MATÉRIEL ===
    
    # Préparation matériel
    dot.node('Preparation', '6. Préparer matériel\n(Sélection + décharge)', 
             **node_styles['process'], fillcolor=roles_colors['Gestionnaire_Info'])
    
    # Affectation
    dot.node('Affectation', '7. Affecter matériel\n(Mise à jour registre)', 
             **node_styles['process'], fillcolor=roles_colors['Gestionnaire_Info'])
    
    # Remise matériel
    dot.node('Remise', '8. Remise matériel\n(Signature décharge)', 
             **node_styles['process'], fillcolor=roles_colors['Employé'])
    
    # === WORKFLOW 3: GESTION COMMANDES ===
    
    # Identification besoin
    dot.node('Besoin', '9. Identifier besoin de commande\n(Analyse demandes)', 
             **node_styles['process'], fillcolor=roles_colors['Gestionnaire_Info'])
    
    # Validation commande
    dot.node('Validation_Commande', '10. Validation et création\n(Bon de commande)', 
             **node_styles['process'], fillcolor=roles_colors['SuperAdmin'])
    
    # Transmission fournisseur
    dot.node('Transmission', '11. Transmission fournisseur\n(Courrier/Fax)', 
             **node_styles['process'], fillcolor=roles_colors['SuperAdmin'])
    
    # Suivi commande
    dot.node('Suivi', '12. Suivi de commande\n(Tableau de suivi)', 
             **node_styles['process'], fillcolor=roles_colors['Secrétaire'])
    
    # === WORKFLOW 4: RÉCEPTION ET CONTRÔLE ===
    
    # Réception physique
    dot.node('Reception', '13. Réception physique\n(Contrôle livraison)', 
             **node_styles['process'], fillcolor=roles_colors['Gestionnaire_Info'])
    
    # Contrôle qualité
    dot.node('Controle', '14. Contrôle qualité\n(Visuel + fonctionnel)', 
             **node_styles['process'], fillcolor=roles_colors['Gestionnaire_Info'])
    
    # Décision conformité
    dot.node('Conforme', 'Livraison conforme ?', 
             **node_styles['decision'], fillcolor=roles_colors['Décision'])
    
    # Correction non-conformité
    dot.node('Correction', '15. Notifier correction\n(Rapport non-conformité)', 
             **node_styles['process'], fillcolor=roles_colors['Système'])
    
    # Procès-verbal
    dot.node('PV', '16. Procès-verbal réception\n(Signature validation)', 
             **node_styles['process'], fillcolor=roles_colors['SuperAdmin'])
    
    # Mise en stock
    dot.node('MiseStock', '17. Mise en stock\n(Numéro inventaire)', 
             **node_styles['process'], fillcolor=roles_colors['Gestionnaire_Info'])
    
    # === WORKFLOW 5: NOTIFICATIONS ET ARCHIVAGE ===
    
    # Notification acteurs
    dot.node('Notification_Acteurs', '18. Notifier acteurs\n(Courrier interne)', 
             **node_styles['process'], fillcolor=roles_colors['Secrétaire'])
    
    # Archivage
    dot.node('Archivage', '19. Archivage documents\n(Classement sécurisé)', 
             **node_styles['process'], fillcolor=roles_colors['Secrétaire'])
    
    # === CONNEXIONS PRINCIPALES ===
    
    # Workflow principal
    dot.edge('Start', 'Demande')
    dot.edge('Demande', 'Enregistrement')
    dot.edge('Enregistrement', 'Stock')
    dot.edge('Stock', 'StockCheck')
    dot.edge('StockCheck', 'Analyse', label='Oui')
    dot.edge('StockCheck', 'Besoin', label='Non')
    dot.edge('Analyse', 'Approval')
    dot.edge('Approval', 'Preparation', label='Oui')
    dot.edge('Approval', 'Notification_Refus', label='Non')
    dot.edge('Notification_Refus', 'End_Refuse')
    dot.edge('Preparation', 'Affectation')
    dot.edge('Affectation', 'Remise')
    dot.edge('Remise', 'End_Approuve')
    
    # Workflow commandes
    dot.edge('Besoin', 'Validation_Commande')
    dot.edge('Validation_Commande', 'Transmission')
    dot.edge('Transmission', 'Suivi')
    dot.edge('Suivi', 'Reception')
    dot.edge('Reception', 'Controle')
    dot.edge('Controle', 'Conforme')
    dot.edge('Conforme', 'PV', label='Oui')
    dot.edge('Conforme', 'Correction', label='Non')
    dot.edge('Correction', 'Suivi')
    dot.edge('PV', 'MiseStock')
    dot.edge('MiseStock', 'Notification_Acteurs')
    dot.edge('Notification_Acteurs', 'Archivage')
    dot.edge('Archivage', 'End_Approuve')
    
    return dot

def create_roles_diagram():
    """Crée un diagramme des rôles et responsabilités."""
    
    dot = Digraph('Roles_ParcInfo', format='png')
    dot.attr(rankdir='LR', size='14,10', dpi='300')
    dot.attr('node', fontname='Arial', fontsize='11', shape='box', style='filled,rounded')
    
    # Couleurs par rôle
    colors = {
        'Employé': '#E3F2FD',
        'Secrétaire': '#F3E5F5', 
        'Gestionnaire_Info': '#E8F5E8',
        'Gestionnaire_Bureau': '#FFF3E0',
        'SuperAdmin': '#F1F8E9'
    }
    
    # Rôles principaux
    dot.node('Employe', '👤 EMPLOYÉ\n• Créer demandes\n• Signer décharges\n• Réceptionner matériel', 
             fillcolor=colors['Employé'])
    
    dot.node('Secretaire', '📋 SECRÉTAIRE\n• Enregistrer demandes\n• Notifications\n• Archivage', 
             fillcolor=colors['Secrétaire'])
    
    dot.node('GestInfo', '💻 GESTIONNAIRE INFO\n• Traiter demandes info\n• Gérer stock info\n• Commandes info', 
             fillcolor=colors['Gestionnaire_Info'])
    
    dot.node('GestBureau', '📁 GESTIONNAIRE BUREAU\n• Traiter demandes bureau\n• Gérer stock bureau\n• Commandes bureau', 
             fillcolor=colors['Gestionnaire_Bureau'])
    
    dot.node('SuperAdmin', '🔧 SUPER ADMIN\n• Validation commandes\n• Gestion fournisseurs\n• Supervision générale', 
             fillcolor=colors['SuperAdmin'])
    
    # Connexions hiérarchiques
    dot.edge('Employe', 'Secretaire')
    dot.edge('Secretaire', 'GestInfo')
    dot.edge('Secretaire', 'GestBureau')
    dot.edge('GestInfo', 'SuperAdmin')
    dot.edge('GestBureau', 'SuperAdmin')
    
    return dot

def main():
    """Fonction principale."""
    
    print("🔄 Génération des diagrammes ParcInfo...")
    
    # Vérifier si Graphviz est installé
    try:
        from graphviz import Digraph
    except ImportError:
        print("❌ Erreur: Graphviz n'est pas installé.")
        print("📦 Installation: pip install graphviz")
        print("💻 Assurez-vous aussi que Graphviz est installé sur votre système:")
        print("   - macOS: brew install graphviz")
        print("   - Ubuntu: sudo apt-get install graphviz")
        print("   - Windows: télécharger depuis https://graphviz.org/")
        return
    
    # Créer le répertoire de sortie
    output_dir = 'diagrammes_generes'
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Générer le workflow principal
        print("📊 Génération du workflow principal...")
        workflow_dot = create_workflow_diagram()
        workflow_file = os.path.join(output_dir, 'workflow_parcinfo_complet')
        workflow_dot.render(workflow_file, view=False, cleanup=True)
        print(f"✅ Workflow principal généré: {workflow_file}.png")
        
        # Générer le diagramme des rôles
        print("👥 Génération du diagramme des rôles...")
        roles_dot = create_roles_diagram()
        roles_file = os.path.join(output_dir, 'roles_parcinfo')
        roles_dot.render(roles_file, view=False, cleanup=True)
        print(f"✅ Diagramme des rôles généré: {roles_file}.png")
        
        print("\n🎉 Génération terminée avec succès!")
        print(f"📁 Fichiers générés dans: {output_dir}/")
        print("📋 Fichiers créés:")
        print(f"   - {workflow_file}.png (Workflow complet)")
        print(f"   - {roles_file}.png (Rôles et responsabilités)")
        
        # Ouvrir les fichiers générés
        if sys.platform == "darwin":  # macOS
            os.system(f"open {workflow_file}.png")
            os.system(f"open {roles_file}.png")
        elif sys.platform == "win32":  # Windows
            os.system(f"start {workflow_file}.png")
            os.system(f"start {roles_file}.png")
        else:  # Linux
            os.system(f"xdg-open {workflow_file}.png")
            os.system(f"xdg-open {roles_file}.png")
            
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        print("💡 Vérifiez que Graphviz est correctement installé sur votre système.")

if __name__ == "__main__":
    main()
