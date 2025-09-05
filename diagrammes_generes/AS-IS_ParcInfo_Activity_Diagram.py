#!/usr/bin/env python3
"""
Générateur de diagramme AS-IS pour ParcInfo
Basé sur l'exemple CHP fourni avec des swimlanes pour les différents rôles
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np
from datetime import datetime

def create_as_is_diagram():
    """Crée le diagramme AS-IS de ParcInfo"""
    
    # Configuration de la figure
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Couleurs
    colors = {
        'employe': '#E3F2FD',      # Bleu clair
        'gestionnaire': '#F3E5F5',  # Violet clair
        'super_admin': '#E8F5E8',   # Vert clair
        'system': '#FFF3E0',        # Orange clair
        'decision': '#FFEBEE',      # Rouge clair
        'start_end': '#424242'      # Gris foncé
    }
    
    # Titre
    ax.text(5, 11.5, 'Activity1: ParcInfo (AS-IS)', 
            fontsize=20, fontweight='bold', ha='center',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='white', edgecolor='gray'))
    
    # Définition des swimlanes
    swimlanes = [
        {'name': 'Employé', 'y_min': 9, 'y_max': 11, 'color': colors['employe']},
        {'name': 'Gestionnaire', 'y_min': 6, 'y_max': 8.5, 'color': colors['gestionnaire']},
        {'name': 'Super Admin', 'y_min': 3, 'y_max': 5.5, 'color': colors['super_admin']},
        {'name': 'Système', 'y_min': 0.5, 'y_max': 2.5, 'color': colors['system']}
    ]
    
    # Dessiner les swimlanes
    for i, lane in enumerate(swimlanes):
        # Rectangle de la swimlane
        rect = FancyBboxPatch((0, lane['y_min']), 10, lane['y_max'] - lane['y_min'],
                             boxstyle="round,pad=0.1", 
                             facecolor=lane['color'], 
                             edgecolor='gray', 
                             linewidth=1)
        ax.add_patch(rect)
        
        # Titre de la swimlane
        ax.text(0.5, (lane['y_min'] + lane['y_max']) / 2, lane['name'],
                fontsize=14, fontweight='bold', ha='center', va='center',
                rotation=90, bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor='gray'))
    
    # Définition des activités par swimlane
    activities = {
        'employe': [
            {'x': 1.5, 'y': 10.2, 'text': 'Créer demande\nd\'équipement', 'type': 'activity'},
            {'x': 3.5, 'y': 10.2, 'text': 'Consulter statut\ndemande', 'type': 'activity'},
            {'x': 5.5, 'y': 10.2, 'text': 'Signer décharge\ndigitale', 'type': 'activity'},
            {'x': 7.5, 'y': 10.2, 'text': 'Réceptionner\nmatériel', 'type': 'activity'},
            {'x': 2.5, 'y': 9.5, 'text': 'Demande\nconforme ?', 'type': 'decision'},
            {'x': 4.5, 'y': 9.5, 'text': 'Matériel\ndisponible ?', 'type': 'decision'},
        ],
        'gestionnaire': [
            {'x': 1.5, 'y': 7.8, 'text': 'Recevoir notification\ndemande', 'type': 'activity'},
            {'x': 3.5, 'y': 7.8, 'text': 'Analyser demande\net budget', 'type': 'activity'},
            {'x': 5.5, 'y': 7.8, 'text': 'Approuver/Refuser\ndemande', 'type': 'activity'},
            {'x': 7.5, 'y': 7.8, 'text': 'Sélectionner\nmatériel', 'type': 'activity'},
            {'x': 2.5, 'y': 7.1, 'text': 'Budget\nsuffisant ?', 'type': 'decision'},
            {'x': 4.5, 'y': 7.1, 'text': 'Demande\njustifiée ?', 'type': 'decision'},
            {'x': 6.5, 'y': 7.1, 'text': 'Stock\ndisponible ?', 'type': 'decision'},
        ],
        'super_admin': [
            {'x': 1.5, 'y': 5.3, 'text': 'Superviser\nprocessus', 'type': 'activity'},
            {'x': 3.5, 'y': 5.3, 'text': 'Valider commandes\nimportantes', 'type': 'activity'},
            {'x': 5.5, 'y': 5.3, 'text': 'Gérer fournisseurs\net contrats', 'type': 'activity'},
            {'x': 7.5, 'y': 5.3, 'text': 'Analyser rapports\net KPIs', 'type': 'activity'},
            {'x': 2.5, 'y': 4.6, 'text': 'Commande >\nseuil ?', 'type': 'decision'},
            {'x': 4.5, 'y': 4.6, 'text': 'Fournisseur\napprouvé ?', 'type': 'decision'},
        ],
        'system': [
            {'x': 1.5, 'y': 2.8, 'text': 'Vérifier stock\net disponibilité', 'type': 'activity'},
            {'x': 3.5, 'y': 2.8, 'text': 'Générer notifications\nautomatiques', 'type': 'activity'},
            {'x': 5.5, 'y': 2.8, 'text': 'Mettre à jour\nstatuts', 'type': 'activity'},
            {'x': 7.5, 'y': 2.8, 'text': 'Archiver données\net historique', 'type': 'activity'},
            {'x': 2.5, 'y': 2.1, 'text': 'Stock\nsuffisant ?', 'type': 'decision'},
            {'x': 4.5, 'y': 2.1, 'text': 'Notification\nrequise ?', 'type': 'decision'},
        ]
    }
    
    # Dessiner les activités
    for lane_name, lane_activities in activities.items():
        for activity in lane_activities:
            x, y = activity['x'], activity['y']
            text = activity['text']
            
            if activity['type'] == 'activity':
                # Rectangle pour activité
                rect = FancyBboxPatch((x-0.8, y-0.3), 1.6, 0.6,
                                     boxstyle="round,pad=0.1", 
                                     facecolor='white', 
                                     edgecolor='black', 
                                     linewidth=1)
                ax.add_patch(rect)
            elif activity['type'] == 'decision':
                # Losange pour décision
                diamond = patches.Polygon([(x, y+0.3), (x+0.8, y), (x, y-0.3), (x-0.8, y)],
                                        facecolor=colors['decision'], 
                                        edgecolor='black', 
                                        linewidth=1)
                ax.add_patch(diamond)
            
            # Texte
            ax.text(x, y, text, fontsize=8, ha='center', va='center', 
                   bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.8))
    
    # Points de début et fin
    # Début
    start_circle = patches.Circle((1.5, 10.8), 0.2, facecolor=colors['start_end'], edgecolor='black')
    ax.add_patch(start_circle)
    ax.text(1.5, 10.8, 'Start', fontsize=8, ha='center', va='center', color='white', fontweight='bold')
    
    # Fin
    end_circle = patches.Circle((7.5, 2.8), 0.2, facecolor=colors['start_end'], edgecolor='black')
    ax.add_patch(end_circle)
    ax.text(7.5, 2.8, 'End', fontsize=8, ha='center', va='center', color='white', fontweight='bold')
    
    # Flèches de flux principal
    arrows = [
        # Employé
        ((1.5, 10.6), (2.5, 9.8)),  # Start -> Demande conforme
        ((2.5, 9.5), (3.5, 10.2)),  # Demande conforme -> Consulter statut
        ((3.5, 10.2), (4.5, 9.8)),  # Consulter statut -> Matériel disponible
        ((4.5, 9.5), (5.5, 10.2)),  # Matériel disponible -> Signer décharge
        ((5.5, 10.2), (7.5, 10.2)), # Signer décharge -> Réceptionner
        
        # Gestionnaire
        ((3.5, 10.2), (1.5, 8.0)),  # Consulter statut -> Recevoir notification
        ((1.5, 7.8), (2.5, 7.4)),   # Recevoir notification -> Budget suffisant
        ((2.5, 7.1), (3.5, 7.8)),   # Budget suffisant -> Analyser demande
        ((3.5, 7.8), (4.5, 7.4)),   # Analyser demande -> Demande justifiée
        ((4.5, 7.1), (5.5, 7.8)),   # Demande justifiée -> Approuver/Refuser
        ((5.5, 7.8), (6.5, 7.4)),   # Approuver/Refuser -> Stock disponible
        ((6.5, 7.1), (7.5, 7.8)),   # Stock disponible -> Sélectionner matériel
        
        # Super Admin
        ((7.5, 7.8), (1.5, 5.5)),   # Sélectionner matériel -> Superviser processus
        ((1.5, 5.3), (2.5, 4.9)),   # Superviser processus -> Commande > seuil
        ((2.5, 4.6), (3.5, 5.3)),   # Commande > seuil -> Valider commandes
        ((3.5, 5.3), (4.5, 4.9)),   # Valider commandes -> Fournisseur approuvé
        ((4.5, 4.6), (5.5, 5.3)),   # Fournisseur approuvé -> Gérer fournisseurs
        ((5.5, 5.3), (7.5, 5.3)),   # Gérer fournisseurs -> Analyser rapports
        
        # Système
        ((7.5, 5.3), (1.5, 3.0)),   # Analyser rapports -> Vérifier stock
        ((1.5, 2.8), (2.5, 2.4)),   # Vérifier stock -> Stock suffisant
        ((2.5, 2.1), (3.5, 2.8)),   # Stock suffisant -> Générer notifications
        ((3.5, 2.8), (4.5, 2.4)),   # Générer notifications -> Notification requise
        ((4.5, 2.1), (5.5, 2.8)),   # Notification requise -> Mettre à jour statuts
        ((5.5, 2.8), (7.5, 2.8)),   # Mettre à jour statuts -> Archiver données
        ((7.5, 2.8), (7.5, 3.0)),   # Archiver données -> End
    ]
    
    # Dessiner les flèches
    for start, end in arrows:
        arrow = ConnectionPatch(start, end, "data", "data",
                              arrowstyle="->", shrinkA=5, shrinkB=5,
                              mutation_scale=20, fc="black", ec="black", linewidth=1.5)
        ax.add_patch(arrow)
    
    # Flèches de retour (non-conformité)
    return_arrows = [
        ((2.5, 9.2), (1.5, 10.2)),  # Demande non conforme -> Créer demande
        ((4.5, 9.2), (3.5, 10.2)),  # Matériel non disponible -> Consulter statut
        ((2.5, 6.8), (1.5, 7.8)),   # Budget insuffisant -> Recevoir notification
        ((4.5, 6.8), (3.5, 7.8)),   # Demande non justifiée -> Analyser demande
        ((6.5, 6.8), (5.5, 7.8)),   # Stock non disponible -> Approuver/Refuser
    ]
    
    for start, end in return_arrows:
        arrow = ConnectionPatch(start, end, "data", "data",
                              arrowstyle="->", shrinkA=5, shrinkB=5,
                              mutation_scale=15, fc="red", ec="red", linewidth=1,
                              linestyle='--')
        ax.add_patch(arrow)
    
    # Légende
    legend_elements = [
        patches.Patch(color='white', label='Activité'),
        patches.Patch(color=colors['decision'], label='Décision'),
        patches.Patch(color=colors['start_end'], label='Début/Fin'),
    ]
    
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
    
    # Informations du diagramme
    info_text = f"""
    Diagramme AS-IS ParcInfo
    Généré le: {datetime.now().strftime('%d/%m/%Y %H:%M')}
    
    Processus actuels de gestion de parc informatique:
    • Workflow des demandes d'équipement
    • Processus d'approbation hiérarchique
    • Gestion des stocks et fournisseurs
    • Système de notifications automatiques
    """
    
    ax.text(0.5, 0.3, info_text, fontsize=10, ha='left', va='top',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.8))
    
    plt.tight_layout()
    return fig

def save_diagram():
    """Sauvegarde le diagramme AS-IS"""
    fig = create_as_is_diagram()
    
    # Sauvegarder en PNG
    filename_png = 'ParcInfo_AS-IS_Activity_Diagram.png'
    fig.savefig(filename_png, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Diagramme AS-IS sauvegardé: {filename_png}")
    
    # Sauvegarder en PDF
    filename_pdf = 'ParcInfo_AS-IS_Activity_Diagram.pdf'
    fig.savefig(filename_pdf, bbox_inches='tight', facecolor='white')
    print(f"✅ Diagramme AS-IS sauvegardé: {filename_pdf}")
    
    plt.close(fig)

if __name__ == "__main__":
    print("🔄 Génération du diagramme AS-IS ParcInfo...")
    save_diagram()
    print("🎉 Diagramme AS-IS généré avec succès!")
