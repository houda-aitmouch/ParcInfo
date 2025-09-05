#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de Diagramme BPMN ParcInfo Mis à Jour
=================================================

Ce script génère un diagramme BPMN complet pour le système ParcInfo
incluant toutes les étapes manquantes : archivage, gestion des commandes,
suivi des livraisons, gestion du matériel et suivi des garanties.

Auteur: Équipe ParcInfo
Date: 2025-01-15
"""

from graphviz import Digraph
import os
import sys

def create_updated_bpmn_diagram():
    """Crée le diagramme BPMN ParcInfo complet avec toutes les étapes."""
    
    # Création du graphe principal
    dot = Digraph('BPMN_ParcInfo_Complet', format='png')
    dot.attr(rankdir='TB', size='20,16', dpi='300')
    dot.attr('node', fontname='Arial', fontsize='9')
    dot.attr('edge', fontname='Arial', fontsize='8')
    
    # Définition des couleurs par rôle
    roles_colors = {
        'Employé': '#E3F2FD',           # Bleu clair
        'Gestionnaire_Info': '#E8F5E8',  # Vert clair
        'Gestionnaire_Bureau': '#FFF3E0', # Orange clair
        'Décision': '#FFE0B2',          # Orange pour les décisions
        'Début_Fin': '#E0E0E0',         # Gris pour début/fin
        'Processus': '#FFF9C4'          # Jaune pour les processus
    }
    
    # Styles des nœuds BPMN
    node_styles = {
        'start_event': {'shape': 'circle', 'style': 'filled', 'width': '0.5', 'height': '0.5'},
        'end_event': {'shape': 'circle', 'style': 'filled', 'width': '0.5', 'height': '0.5'},
        'task': {'shape': 'box', 'style': 'filled,rounded'},
        'gateway': {'shape': 'diamond', 'style': 'filled'},
        'subprocess': {'shape': 'box', 'style': 'filled,rounded', 'peripheries': '2'}
    }
    
    # === NŒUDS DE DÉBUT ET FIN ===
    dot.node('Start', 'DÉBUT\nDemande d\'équipement', 
             **node_styles['start_event'], fillcolor=roles_colors['Début_Fin'])
    dot.node('End', 'FIN\nProcessus terminé', 
             **node_styles['end_event'], fillcolor=roles_colors['Début_Fin'])
    
    # === SWIMLANE EMPLOYÉ ===
    dot.node('Demande_Papier', 'Soumet demande d\'équipement\nvia formulaire papier', 
             **node_styles['task'], fillcolor=roles_colors['Employé'])
    
    dot.node('Signature_Reception', 'Signature de la décharge\net réception du matériel', 
             **node_styles['task'], fillcolor=roles_colors['Employé'])
    
    # === SWIMLANE GESTIONNAIRE INFORMATIQUE ===
    dot.node('Reception_Info', 'Réception & Vérification\ndemande équipement informatique', 
             **node_styles['task'], fillcolor=roles_colors['Gestionnaire_Info'])
    
    dot.node('Verif_Stock_Info', 'Vérification stock informatique', 
             **node_styles['task'], fillcolor=roles_colors['Gestionnaire_Info'])
    
    dot.node('Decision_Approbation_Info', 'Décision d\'approbation', 
             **node_styles['task'], fillcolor=roles_colors['Gestionnaire_Info'])
    
    dot.node('Preparation_Decharge_Info', 'Préparation décharge papier', 
             **node_styles['task'], fillcolor=roles_colors['Gestionnaire_Info'])
    
    dot.node('Demande_Rejetee_Info', 'Demande rejetée\n- Stock insuffisant', 
             **node_styles['task'], fillcolor=roles_colors['Gestionnaire_Info'])
    
    # === SWIMLANE GESTIONNAIRE BUREAUTIQUE ===
    dot.node('Reception_Bureau', 'Réception & Vérification\ndemande équipement bureautique', 
             **node_styles['task'], fillcolor=roles_colors['Gestionnaire_Bureau'])
    
    dot.node('Verif_Stock_Bureau', 'Vérification stock bureautique', 
             **node_styles['task'], fillcolor=roles_colors['Gestionnaire_Bureau'])
    
    dot.node('Decision_Approbation_Bureau', 'Décision d\'approbation', 
             **node_styles['task'], fillcolor=roles_colors['Gestionnaire_Bureau'])
    
    dot.node('Preparation_Decharge_Bureau', 'Préparation décharge papier', 
             **node_styles['task'], fillcolor=roles_colors['Gestionnaire_Bureau'])
    
    dot.node('Demande_Rejetee_Bureau', 'Demande rejetée\n- Stock insuffisant', 
             **node_styles['task'], fillcolor=roles_colors['Gestionnaire_Bureau'])
    
    # === GATEWAYS DE DÉCISION ===
    dot.node('Gateway_Type_Equipement', 'Type d\'équipement ?', 
             **node_styles['gateway'], fillcolor=roles_colors['Décision'])
    
    dot.node('Gateway_Stock_Info', 'Stock suffisant ?', 
             **node_styles['gateway'], fillcolor=roles_colors['Décision'])
    
    dot.node('Gateway_Stock_Bureau', 'Stock suffisant ?', 
             **node_styles['gateway'], fillcolor=roles_colors['Décision'])
    
    dot.node('Gateway_Approbation_Info', 'Approuver ?', 
             **node_styles['gateway'], fillcolor=roles_colors['Décision'])
    
    dot.node('Gateway_Approbation_Bureau', 'Approuver ?', 
             **node_styles['gateway'], fillcolor=roles_colors['Décision'])
    
    # === NOUVELLES ÉTAPES AJOUTÉES ===
    
    # Archivage après signature
    dot.node('Archivage_Decharge', 'Archivage de la décharge\ndans dossier/fichier', 
             **node_styles['task'], fillcolor=roles_colors['Processus'])
    
    # Gestion des commandes
    dot.node('Gestion_Commandes', 'Gestion des commandes\n- Papier ou fichier\n- Détail matériel, quantité,\n  prix, coût total', 
             **node_styles['subprocess'], fillcolor=roles_colors['Processus'])
    
    # Suivi des livraisons
    dot.node('Suivi_Livraisons', 'Suivi des livraisons\n- Note date prévue/réelle\n- Mise à jour état commandes\n  (en attente, en cours,\n   livrée, retardée)\nTout sur fichier manuel', 
             **node_styles['subprocess'], fillcolor=roles_colors['Processus'])
    
    # Gestion du matériel
    dot.node('Gestion_Materiel', 'Gestion du matériel\n- Affectation aux utilisateurs\n- Suivi état matériel\n  (nouveau, affecté, en panne,\n   maintenance)\nTout sur fichier manuel', 
             **node_styles['subprocess'], fillcolor=roles_colors['Processus'])
    
    # Suivi des garanties
    dot.node('Suivi_Garanties', 'Suivi des garanties\n- Début/fin de garantie\n- Actions avant expiration\n- Tout sur fichier manuel', 
             **node_styles['subprocess'], fillcolor=roles_colors['Processus'])
    
    # === CONNEXIONS PRINCIPALES ===
    
    # Début du processus
    dot.edge('Start', 'Demande_Papier')
    dot.edge('Demande_Papier', 'Gateway_Type_Equipement')
    
    # Branchement selon le type d'équipement
    dot.edge('Gateway_Type_Equipement', 'Reception_Info', label='Informatique')
    dot.edge('Gateway_Type_Equipement', 'Reception_Bureau', label='Bureautique')
    
    # Workflow Gestionnaire Informatique
    dot.edge('Reception_Info', 'Verif_Stock_Info')
    dot.edge('Verif_Stock_Info', 'Gateway_Stock_Info')
    dot.edge('Gateway_Stock_Info', 'Decision_Approbation_Info', label='Suffisant')
    dot.edge('Gateway_Stock_Info', 'Demande_Rejetee_Info', label='Insuffisant')
    dot.edge('Decision_Approbation_Info', 'Gateway_Approbation_Info')
    dot.edge('Gateway_Approbation_Info', 'Preparation_Decharge_Info', label='Approuver')
    dot.edge('Gateway_Approbation_Info', 'Demande_Rejetee_Info', label='Rejeter')
    
    # Workflow Gestionnaire Bureautique
    dot.edge('Reception_Bureau', 'Verif_Stock_Bureau')
    dot.edge('Verif_Stock_Bureau', 'Gateway_Stock_Bureau')
    dot.edge('Gateway_Stock_Bureau', 'Decision_Approbation_Bureau', label='Suffisant')
    dot.edge('Gateway_Stock_Bureau', 'Demande_Rejetee_Bureau', label='Insuffisant')
    dot.edge('Decision_Approbation_Bureau', 'Gateway_Approbation_Bureau')
    dot.edge('Gateway_Approbation_Bureau', 'Preparation_Decharge_Bureau', label='Approuver')
    dot.edge('Gateway_Approbation_Bureau', 'Demande_Rejetee_Bureau', label='Rejeter')
    
    # Convergence vers la signature
    dot.edge('Preparation_Decharge_Info', 'Signature_Reception')
    dot.edge('Preparation_Decharge_Bureau', 'Signature_Reception')
    dot.edge('Demande_Rejetee_Info', 'Signature_Reception')
    dot.edge('Demande_Rejetee_Bureau', 'Signature_Reception')
    
    # Archivage après signature
    dot.edge('Signature_Reception', 'Archivage_Decharge')
    
    # Connexion aux processus de gestion
    dot.edge('Archivage_Decharge', 'Gestion_Commandes')
    dot.edge('Gestion_Commandes', 'Suivi_Livraisons')
    dot.edge('Suivi_Livraisons', 'Gestion_Materiel')
    dot.edge('Gestion_Materiel', 'Suivi_Garanties')
    
    # Fin du processus
    dot.edge('Suivi_Garanties', 'End')
    
    return dot

def create_swimlanes_diagram():
    """Crée un diagramme avec les swimlanes clairement définies."""
    
    dot = Digraph('BPMN_ParcInfo_Swimlanes', format='png')
    dot.attr(rankdir='TB', size='24,18', dpi='300')
    dot.attr('node', fontname='Arial', fontsize='10')
    dot.attr('edge', fontname='Arial', fontsize='9')
    
    # Couleurs par swimlane
    colors = {
        'Employé': '#E3F2FD',
        'Gestionnaire_Info': '#E8F5E8',
        'Gestionnaire_Bureau': '#FFF3E0',
        'Processus': '#FFF9C4'
    }
    
    # Création des swimlanes avec subgraphs
    with dot.subgraph(name='cluster_0') as c:
        c.attr(label='👤 EMPLOYÉ', style='filled', fillcolor=colors['Employé'])
        c.attr('node', style='filled,rounded')
        
        c.node('Start_Employee', 'DÉBUT\nDemande d\'équipement')
        c.node('Demande_Employee', 'Soumet demande d\'équipement\nvia formulaire papier')
        c.node('Signature_Employee', 'Signature de la décharge\net réception du matériel')
        c.node('End_Employee', 'FIN\nProcessus terminé')
        
        # Connexions dans la swimlane
        c.edge('Start_Employee', 'Demande_Employee')
        c.edge('Signature_Employee', 'End_Employee')
    
    with dot.subgraph(name='cluster_1') as c:
        c.attr(label='💻 GESTIONNAIRE INFORMATIQUE', style='filled', fillcolor=colors['Gestionnaire_Info'])
        c.attr('node', style='filled,rounded')
        
        c.node('Reception_Info', 'Réception & Vérification\ndemande équipement informatique')
        c.node('Verif_Stock_Info', 'Vérification stock informatique')
        c.node('Decision_Info', 'Décision d\'approbation')
        c.node('Preparation_Info', 'Préparation décharge papier')
        c.node('Rejet_Info', 'Demande rejetée\n- Stock insuffisant')
        
        # Connexions dans la swimlane
        c.edge('Reception_Info', 'Verif_Stock_Info')
        c.edge('Verif_Stock_Info', 'Decision_Info')
        c.edge('Decision_Info', 'Preparation_Info')
        c.edge('Decision_Info', 'Rejet_Info')
    
    with dot.subgraph(name='cluster_2') as c:
        c.attr(label='📁 GESTIONNAIRE BUREAUTIQUE', style='filled', fillcolor=colors['Gestionnaire_Bureau'])
        c.attr('node', style='filled,rounded')
        
        c.node('Reception_Bureau', 'Réception & Vérification\ndemande équipement bureautique')
        c.node('Verif_Stock_Bureau', 'Vérification stock bureautique')
        c.node('Decision_Bureau', 'Décision d\'approbation')
        c.node('Preparation_Bureau', 'Préparation décharge papier')
        c.node('Rejet_Bureau', 'Demande rejetée\n- Stock insuffisant')
        
        # Connexions dans la swimlane
        c.edge('Reception_Bureau', 'Verif_Stock_Bureau')
        c.edge('Verif_Stock_Bureau', 'Decision_Bureau')
        c.edge('Decision_Bureau', 'Preparation_Bureau')
        c.edge('Decision_Bureau', 'Rejet_Bureau')
    
    with dot.subgraph(name='cluster_3') as c:
        c.attr(label='📋 PROCESSUS DE GESTION', style='filled', fillcolor=colors['Processus'])
        c.attr('node', style='filled,rounded')
        
        c.node('Archivage', 'Archivage de la décharge\ndans dossier/fichier')
        c.node('Commandes', 'Gestion des commandes\n- Papier ou fichier\n- Détail matériel, quantité,\n  prix, coût total')
        c.node('Livraisons', 'Suivi des livraisons\n- Note date prévue/réelle\n- Mise à jour état commandes')
        c.node('Materiel', 'Gestion du matériel\n- Affectation aux utilisateurs\n- Suivi état matériel')
        c.node('Garanties', 'Suivi des garanties\n- Début/fin de garantie\n- Actions avant expiration')
        
        # Connexions dans la swimlane
        c.edge('Archivage', 'Commandes')
        c.edge('Commandes', 'Livraisons')
        c.edge('Livraisons', 'Materiel')
        c.edge('Materiel', 'Garanties')
    
    # Connexions entre swimlanes
    dot.edge('Demande_Employee', 'Reception_Info')
    dot.edge('Demande_Employee', 'Reception_Bureau')
    dot.edge('Preparation_Info', 'Signature_Employee')
    dot.edge('Preparation_Bureau', 'Signature_Employee')
    dot.edge('Rejet_Info', 'Signature_Employee')
    dot.edge('Rejet_Bureau', 'Signature_Employee')
    dot.edge('Signature_Employee', 'Archivage')
    dot.edge('Garanties', 'End_Employee')
    
    return dot

def main():
    """Fonction principale."""
    
    print("🔄 Génération du diagramme BPMN ParcInfo mis à jour...")
    
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
        # Générer le diagramme BPMN principal
        print("📊 Génération du diagramme BPMN principal...")
        bpmn_dot = create_updated_bpmn_diagram()
        bpmn_file = os.path.join(output_dir, 'bpmn_parcinfo_complet')
        bpmn_dot.render(bpmn_file, view=False, cleanup=True)
        print(f"✅ Diagramme BPMN principal généré: {bpmn_file}.png")
        
        # Générer le diagramme avec swimlanes
        print("🏊 Génération du diagramme avec swimlanes...")
        swimlanes_dot = create_swimlanes_diagram()
        swimlanes_file = os.path.join(output_dir, 'bpmn_parcinfo_swimlanes')
        swimlanes_dot.render(swimlanes_file, view=False, cleanup=True)
        print(f"✅ Diagramme avec swimlanes généré: {swimlanes_file}.png")
        
        print("\n🎉 Génération terminée avec succès!")
        print(f"📁 Fichiers générés dans: {output_dir}/")
        print("📋 Fichiers créés:")
        print(f"   - {bpmn_file}.png (Diagramme BPMN complet)")
        print(f"   - {swimlanes_file}.png (Diagramme avec swimlanes)")
        
        print("\n🔍 NOUVELLES ÉTAPES AJOUTÉES:")
        print("   ✅ Archivage de la décharge après signature")
        print("   ✅ Gestion des commandes (papier/fichier)")
        print("   ✅ Suivi des livraisons avec dates et états")
        print("   ✅ Gestion du matériel et affectation")
        print("   ✅ Suivi des garanties et expiration")
        
        # Ouvrir les fichiers générés
        if sys.platform == "darwin":  # macOS
            os.system(f"open {bpmn_file}.png")
            os.system(f"open {swimlanes_file}.png")
        elif sys.platform == "win32":  # Windows
            os.system(f"start {bpmn_file}.png")
            os.system(f"start {swimlanes_file}.png")
        else:  # Linux
            os.system(f"xdg-open {bpmn_file}.png")
            os.system(f"xdg-open {swimlanes_file}.png")
            
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        print("💡 Vérifiez que Graphviz est correctement installé sur votre système.")

if __name__ == "__main__":
    main()
