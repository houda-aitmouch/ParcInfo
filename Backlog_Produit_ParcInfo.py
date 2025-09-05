#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de génération du Backlog Produit ParcInfo
Génère un fichier Excel avec toutes les fonctionnalités du système
"""

import pandas as pd
from datetime import datetime
import os

def create_backlog_excel():
    """Crée le fichier Excel du backlog produit"""
    
    # Données du backlog
    backlog_data = [
        # EPIC: Authentification
        {
            'Prio': 'P1', 'EPIC': 'Authentification', 'Feature': 'Interface de connexion', 
            'Persona': 'Employé', 'Macro US': 'En tant qu\'utilisateur, je veux me connecter au système pour accéder à mes fonctionnalités',
            'RG': 'RG-AUTH-001: Champs identifiant et mot de passe obligatoires',
            'US': 'US-AUTH-001: Saisir mon identifiant et mot de passe pour me connecter',
            'Dépendance': '-', 'Statut': 'À faire', 'Commentaire': 'Interface responsive et sécurisée',
            'Feature Link': '/users/login/', 'US Link': '/users/login/'
        },
        {
            'Prio': 'P1', 'EPIC': 'Authentification', 'Feature': 'Gestion des sessions', 
            'Persona': 'Employé', 'Macro US': 'En tant qu\'utilisateur, je veux rester connecté pendant ma session de travail',
            'RG': 'RG-AUTH-002: Session valide pendant 8h d\'inactivité',
            'US': 'US-AUTH-002: Ma session reste active pendant mon travail',
            'Dépendance': '-', 'Statut': 'À faire', 'Commentaire': 'Timeout configurable',
            'Feature Link': '/users/logout/', 'US Link': '/users/logout/'
        },
        {
            'Prio': 'P1', 'EPIC': 'Authentification', 'Feature': 'Redirection par rôle', 
            'Persona': 'Employé', 'Macro US': 'En tant qu\'utilisateur, je veux être redirigé vers mon dashboard approprié',
            'RG': 'RG-AUTH-003: Redirection selon le groupe utilisateur',
            'US': 'US-AUTH-003: Accéder directement à mon espace de travail',
            'Dépendance': '-', 'Statut': 'À faire', 'Commentaire': 'Dashboard personnalisé par rôle',
            'Feature Link': '/users/redirect-user/', 'US Link': '/users/redirect-user/'
        },
        
        # EPIC: Gestion Utilisateurs
        {
            'Prio': 'P1', 'EPIC': 'Gestion Utilisateurs', 'Feature': 'Profil utilisateur', 
            'Persona': 'Employé', 'Macro US': 'En tant qu\'utilisateur, je veux consulter et modifier mon profil',
            'RG': 'RG-USER-001: Données personnelles modifiables',
            'US': 'US-USER-001: Voir mes informations personnelles',
            'Dépendance': 'Authentification', 'Statut': 'À faire', 'Commentaire': 'Gestion des données personnelles',
            'Feature Link': '/users/profil/', 'US Link': '/users/profil/'
        },
        {
            'Prio': 'P1', 'EPIC': 'Gestion Utilisateurs', 'Feature': 'Gestion des rôles', 
            'Persona': 'Super Admin', 'Macro US': 'En tant qu\'admin, je veux gérer les rôles et permissions',
            'RG': 'RG-USER-002: 4 rôles distincts avec permissions spécifiques',
            'US': 'US-USER-002: Créer/modifier les groupes d\'utilisateurs',
            'Dépendance': 'Authentification', 'Statut': 'À faire', 'Commentaire': 'Rôles: Employé, Gestionnaire Info, Gestionnaire Bureau, Super Admin',
            'Feature Link': '/users/superadmin/', 'US Link': '/users/superadmin/'
        },
        
        # EPIC: Demandes Équipement
        {
            'Prio': 'P1', 'EPIC': 'Demandes Équipement', 'Feature': 'Création de demande', 
            'Persona': 'Employé', 'Macro US': 'En tant qu\'employé, je veux créer une demande d\'équipement',
            'RG': 'RG-DEM-001: Champs obligatoires selon le type',
            'US': 'US-DEM-001: Remplir le formulaire de demande',
            'Dépendance': 'Authentification', 'Statut': 'À faire', 'Commentaire': 'Formulaire dynamique selon catégorie',
            'Feature Link': '/demande_equipement/nouvelle/', 'US Link': '/demande_equipement/nouvelle/'
        },
        {
            'Prio': 'P1', 'EPIC': 'Demandes Équipement', 'Feature': 'Consultation des demandes', 
            'Persona': 'Employé', 'Macro US': 'En tant qu\'employé, je veux voir mes demandes',
            'RG': 'RG-DEM-002: Seules mes demandes visibles',
            'US': 'US-DEM-002: Lister mes demandes avec statuts',
            'Dépendance': 'Authentification', 'Statut': 'À faire', 'Commentaire': 'Filtrage par statut et date',
            'Feature Link': '/demande_equipement/', 'US Link': '/demande_equipement/'
        },
        {
            'Prio': 'P1', 'EPIC': 'Demandes Équipement', 'Feature': 'Approbation des demandes', 
            'Persona': 'Gestionnaire Info', 'Macro US': 'En tant que gestionnaire, je veux approuver/rejeter les demandes',
            'RG': 'RG-DEM-003: Validation selon budget et disponibilité',
            'US': 'US-DEM-003: Traiter les demandes en attente',
            'Dépendance': 'Création de demande', 'Statut': 'À faire', 'Commentaire': 'Workflow d\'approbation',
            'Feature Link': '/demande_equipement/approuver/<id>/', 'US Link': '/demande_equipement/approuver/<id>/'
        },
        {
            'Prio': 'P1', 'EPIC': 'Demandes Équipement', 'Feature': 'Signature de décharge', 
            'Persona': 'Employé', 'Macro US': 'En tant qu\'employé, je veux signer ma décharge',
            'RG': 'RG-DEM-004: Signature obligatoire avant réception',
            'US': 'US-DEM-004: Signer électroniquement ma décharge',
            'Dépendance': 'Approbation de demande', 'Statut': 'À faire', 'Commentaire': 'Signature électronique sécurisée',
            'Feature Link': '/demande_equipement/signer-decharge/<id>/', 'US Link': '/demande_equipement/signer-decharge/<id>/'
        },
        
        # EPIC: Matériel Informatique
        {
            'Prio': 'P1', 'EPIC': 'Matériel Informatique', 'Feature': 'Gestion du parc', 
            'Persona': 'Gestionnaire Info', 'Macro US': 'En tant que gestionnaire, je veux gérer le matériel informatique',
            'RG': 'RG-MAT-001: Inventaire complet avec codes uniques',
            'US': 'US-MAT-001: Ajouter/modifier/supprimer du matériel',
            'Dépendance': '-', 'Statut': 'À faire', 'Commentaire': 'Codes d\'inventaire automatiques',
            'Feature Link': '/materiel_informatique/', 'US Link': '/materiel_informatique/'
        },
        {
            'Prio': 'P1', 'EPIC': 'Matériel Informatique', 'Feature': 'Affectation d\'équipements', 
            'Persona': 'Gestionnaire Info', 'Macro US': 'En tant que gestionnaire, je veux affecter des équipements',
            'RG': 'RG-MAT-002: Un équipement par utilisateur maximum',
            'US': 'US-MAT-002: Assigner un équipement à un utilisateur',
            'Dépendance': 'Gestion du parc', 'Statut': 'À faire', 'Commentaire': 'Traçabilité des affectations',
            'Feature Link': '/materiel_informatique/', 'US Link': '/materiel_informatique/'
        },
        
        # EPIC: Matériel Bureau
        {
            'Prio': 'P1', 'EPIC': 'Matériel Bureau', 'Feature': 'Gestion du mobilier', 
            'Persona': 'Gestionnaire Bureau', 'Macro US': 'En tant que gestionnaire bureau, je veux gérer le mobilier',
            'RG': 'RG-MAT-003: Inventaire bureau avec localisation',
            'US': 'US-MAT-003: Gérer le mobilier de bureau',
            'Dépendance': '-', 'Statut': 'À faire', 'Commentaire': 'Gestion des espaces de travail',
            'Feature Link': '/materiel_bureautique/', 'US Link': '/materiel_bureautique/'
        },
        {
            'Prio': 'P1', 'EPIC': 'Matériel Bureau', 'Feature': 'Affectation mobilier', 
            'Persona': 'Gestionnaire Bureau', 'Macro US': 'En tant que gestionnaire bureau, je veux affecter du mobilier',
            'RG': 'RG-MAT-004: Mobilier selon poste de travail',
            'US': 'US-MAT-004: Assigner du mobilier aux employés',
            'Dépendance': 'Gestion du mobilier', 'Statut': 'À faire', 'Commentaire': 'Configuration poste de travail',
            'Feature Link': '/materiel_bureautique/', 'US Link': '/materiel_bureautique/'
        },
        
        # EPIC: Commandes Informatiques
        {
            'Prio': 'P1', 'EPIC': 'Commandes Informatiques', 'Feature': 'Création de commande', 
            'Persona': 'Gestionnaire Info', 'Macro US': 'En tant que gestionnaire, je veux créer des commandes informatiques',
            'RG': 'RG-COM-001: Validation fournisseur et budget',
            'US': 'US-COM-001: Créer une commande avec lignes',
            'Dépendance': 'Gestion du parc', 'Statut': 'À faire', 'Commentaire': 'Gestion des devis et budgets',
            'Feature Link': '/commande_informatique/ajouter/', 'US Link': '/commande_informatique/ajouter/'
        },
        {
            'Prio': 'P1', 'EPIC': 'Commandes Informatiques', 'Feature': 'Suivi des commandes', 
            'Persona': 'Gestionnaire Info', 'Macro US': 'En tant que gestionnaire, je veux suivre mes commandes',
            'RG': 'RG-COM-002: Statuts de commande obligatoires',
            'US': 'US-COM-002: Voir l\'état de mes commandes',
            'Dépendance': 'Création de commande', 'Statut': 'À faire', 'Commentaire': 'Workflow de commande',
            'Feature Link': '/commande_informatique/liste/', 'US Link': '/commande_informatique/liste/'
        },
        
        # EPIC: Commandes Bureau
        {
            'Prio': 'P1', 'EPIC': 'Commandes Bureau', 'Feature': 'Création commande bureau', 
            'Persona': 'Gestionnaire Bureau', 'Macro US': 'En tant que gestionnaire bureau, je veux commander du mobilier',
            'RG': 'RG-COM-003: Validation fournisseur bureau',
            'US': 'US-COM-003: Créer commande mobilier',
            'Dépendance': 'Gestion du mobilier', 'Statut': 'À faire', 'Commentaire': 'Catalogue fournisseurs bureau',
            'Feature Link': '/commande_bureau/ajouter/', 'US Link': '/commande_bureau/ajouter/'
        },
        {
            'Prio': 'P1', 'EPIC': 'Commandes Bureau', 'Feature': 'Suivi commandes bureau', 
            'Persona': 'Gestionnaire Bureau', 'Macro US': 'En tant que gestionnaire bureau, je veux suivre mes commandes',
            'RG': 'RG-COM-004: Statuts spécifiques bureau',
            'US': 'US-COM-004: Suivre commandes mobilier',
            'Dépendance': 'Création commande bureau', 'Statut': 'À faire', 'Commentaire': 'Gestion des délais livraison',
            'Feature Link': '/commande_bureau/liste/', 'US Link': '/commande_bureau/liste/'
        },
        
        # EPIC: Fournisseurs
        {
            'Prio': 'P1', 'EPIC': 'Fournisseurs', 'Feature': 'Gestion catalogue', 
            'Persona': 'Super Admin', 'Macro US': 'En tant qu\'admin, je veux gérer les fournisseurs',
            'RG': 'RG-FOU-001: Données fournisseur complètes',
            'US': 'US-FOU-001: Ajouter/modifier fournisseurs',
            'Dépendance': '-', 'Statut': 'À faire', 'Commentaire': 'Base de données fournisseurs',
            'Feature Link': '/fournisseurs/', 'US Link': '/fournisseurs/'
        },
        {
            'Prio': 'P1', 'EPIC': 'Fournisseurs', 'Feature': 'Catalogue produits', 
            'Persona': 'Super Admin', 'Macro US': 'En tant qu\'admin, je veux gérer les catalogues',
            'RG': 'RG-FOU-002: Désignations et descriptions',
            'US': 'US-FOU-002: Maintenir les catalogues produits',
            'Dépendance': 'Gestion catalogue', 'Statut': 'À faire', 'Commentaire': 'Classification produits',
            'Feature Link': '/fournisseurs/', 'US Link': '/fournisseurs/'
        },
        
        # EPIC: Livraisons
        {
            'Prio': 'P1', 'EPIC': 'Livraisons', 'Feature': 'Réception de livraisons', 
            'Persona': 'Gestionnaire Info', 'Macro US': 'En tant que gestionnaire, je veux réceptionner les livraisons',
            'RG': 'RG-LIV-001: PV de réception obligatoire',
            'US': 'US-LIV-001: Valider les livraisons reçues',
            'Dépendance': 'Commandes', 'Statut': 'À faire', 'Commentaire': 'Contrôle qualité réception',
            'Feature Link': '/livraison/nouvelle/', 'US Link': '/livraison/nouvelle/'
        },
        {
            'Prio': 'P1', 'EPIC': 'Livraisons', 'Feature': 'Suivi des livraisons', 
            'Persona': 'Gestionnaire Info', 'Macro US': 'En tant que gestionnaire, je veux suivre les livraisons',
            'RG': 'RG-LIV-002: Statuts de livraison',
            'US': 'US-LIV-002: Voir l\'état des livraisons',
            'Dépendance': 'Réception de livraisons', 'Statut': 'À faire', 'Commentaire': 'Traçabilité complète',
            'Feature Link': '/livraison/', 'US Link': '/livraison/'
        },
        
        # EPIC: Notifications (P2)
        {
            'Prio': 'P2', 'EPIC': 'Notifications', 'Feature': 'Système de notifications', 
            'Persona': 'Employé', 'Macro US': 'En tant qu\'utilisateur, je veux recevoir des notifications',
            'RG': 'RG-NOT-001: Notifications temps réel',
            'US': 'US-NOT-001: Voir mes notifications',
            'Dépendance': 'Demandes Équipement', 'Statut': 'À faire', 'Commentaire': 'Notifications push et email',
            'Feature Link': '/users/notifications-demandes/', 'US Link': '/users/notifications-demandes/'
        },
        {
            'Prio': 'P2', 'EPIC': 'Notifications', 'Feature': 'Notifications garantie', 
            'Persona': 'Employé', 'Macro US': 'En tant qu\'utilisateur, je veux être alerté des garanties',
            'RG': 'RG-NOT-002: Alertes 30 jours avant expiration',
            'US': 'US-NOT-002: Recevoir alertes garantie',
            'Dépendance': 'Matériel Informatique', 'Statut': 'À faire', 'Commentaire': 'Système d\'alertes automatiques',
            'Feature Link': '/users/notifications-garantie/', 'US Link': '/users/notifications-garantie/'
        },
        
        # EPIC: Dashboard (P2)
        {
            'Prio': 'P2', 'EPIC': 'Dashboard', 'Feature': 'Tableau de bord employé', 
            'Persona': 'Employé', 'Macro US': 'En tant qu\'employé, je veux voir mon dashboard',
            'RG': 'RG-DASH-001: Données personnalisées par rôle',
            'US': 'US-DASH-001: Accéder à mon tableau de bord',
            'Dépendance': 'Authentification', 'Statut': 'À faire', 'Commentaire': 'Vue d\'ensemble personnalisée',
            'Feature Link': '/users/employe/', 'US Link': '/users/employe/'
        },
        {
            'Prio': 'P2', 'EPIC': 'Dashboard', 'Feature': 'Dashboard gestionnaire info', 
            'Persona': 'Gestionnaire Info', 'Macro US': 'En tant que gestionnaire, je veux mon dashboard',
            'RG': 'RG-DASH-002: Métriques informatiques',
            'US': 'US-DASH-002: Voir les KPIs informatiques',
            'Dépendance': 'Authentification', 'Statut': 'À faire', 'Commentaire': 'Indicateurs de performance',
            'Feature Link': '/users/gestionnaire_info/', 'US Link': '/users/gestionnaire_info/'
        },
        {
            'Prio': 'P2', 'EPIC': 'Dashboard', 'Feature': 'Dashboard gestionnaire bureau', 
            'Persona': 'Gestionnaire Bureau', 'Macro US': 'En tant que gestionnaire bureau, je veux mon dashboard',
            'RG': 'RG-DASH-003: Métriques bureau',
            'US': 'US-DASH-003: Voir les KPIs bureau',
            'Dépendance': 'Authentification', 'Statut': 'À faire', 'Commentaire': 'Indicateurs bureau',
            'Feature Link': '/users/gestionnaire_bureau/', 'US Link': '/users/gestionnaire_bureau/'
        },
        {
            'Prio': 'P2', 'EPIC': 'Dashboard', 'Feature': 'Dashboard super admin', 
            'Persona': 'Super Admin', 'Macro US': 'En tant qu\'admin, je veux le dashboard complet',
            'RG': 'RG-DASH-004: Vue globale du système',
            'US': 'US-DASH-004: Accéder à toutes les données',
            'Dépendance': 'Authentification', 'Statut': 'À faire', 'Commentaire': 'Administration complète',
            'Feature Link': '/users/superadmin/', 'US Link': '/users/superadmin/'
        },
        
        # EPIC: Chatbot (P2)
        {
            'Prio': 'P2', 'EPIC': 'Chatbot', 'Feature': 'Assistant IA', 
            'Persona': 'Employé', 'Macro US': 'En tant qu\'utilisateur, je veux poser des questions',
            'RG': 'RG-CHAT-001: Réponses basées sur la base de connaissances',
            'US': 'US-CHAT-001: Interroger l\'assistant IA',
            'Dépendance': '-', 'Statut': 'À faire', 'Commentaire': 'RAG avec base de connaissances',
            'Feature Link': '/chatbot/', 'US Link': '/chatbot/'
        },
        {
            'Prio': 'P2', 'EPIC': 'Chatbot', 'Feature': 'Base de connaissances', 
            'Persona': 'Super Admin', 'Macro US': 'En tant qu\'admin, je veux maintenir la base',
            'RG': 'RG-CHAT-002: Documentation à jour',
            'US': 'US-CHAT-002: Mettre à jour la documentation',
            'Dépendance': 'Assistant IA', 'Statut': 'À faire', 'Commentaire': 'Système RAG avancé',
            'Feature Link': '/chatbot/', 'US Link': '/chatbot/'
        },
        
        # EPIC: Rapports (P2)
        {
            'Prio': 'P2', 'EPIC': 'Rapports', 'Feature': 'Export Excel', 
            'Persona': 'Gestionnaire Info', 'Macro US': 'En tant que gestionnaire, je veux exporter des données',
            'RG': 'RG-RAP-001: Formats Excel standardisés',
            'US': 'US-RAP-001: Exporter les données en Excel',
            'Dépendance': 'Gestion du parc', 'Statut': 'À faire', 'Commentaire': 'Templates Excel personnalisés',
            'Feature Link': '/materiel_informatique/export_excel/', 'US Link': '/materiel_informatique/export_excel/'
        },
        {
            'Prio': 'P2', 'EPIC': 'Rapports', 'Feature': 'Rapports de livraison', 
            'Persona': 'Gestionnaire Info', 'Macro US': 'En tant que gestionnaire, je veux des rapports',
            'RG': 'RG-RAP-002: Statistiques de livraison',
            'US': 'US-RAP-002: Générer des rapports',
            'Dépendance': 'Livraisons', 'Statut': 'À faire', 'Commentaire': 'Tableaux de bord analytiques',
            'Feature Link': '/livraison/rapports/', 'US Link': '/livraison/rapports/'
        },
        
        # EPIC: Recherche (P2)
        {
            'Prio': 'P2', 'EPIC': 'Recherche', 'Feature': 'Recherche globale', 
            'Persona': 'Employé', 'Macro US': 'En tant qu\'utilisateur, je veux rechercher',
            'RG': 'RG-RECH-001: Recherche multi-critères',
            'US': 'US-RECH-001: Trouver rapidement des informations',
            'Dépendance': '-', 'Statut': 'À faire', 'Commentaire': 'Recherche sémantique',
            'Feature Link': '/users/search/', 'US Link': '/users/search/'
        },
        
        # EPIC: Garanties (P3)
        {
            'Prio': 'P3', 'EPIC': 'Garanties', 'Feature': 'Suivi des garanties', 
            'Persona': 'Gestionnaire Info', 'Macro US': 'En tant que gestionnaire, je veux suivre les garanties',
            'RG': 'RG-GAR-001: Alertes automatiques',
            'US': 'US-GAR-001: Gérer les garanties',
            'Dépendance': 'Matériel Informatique', 'Statut': 'À faire', 'Commentaire': 'Système d\'alertes',
            'Feature Link': '/users/dashboard-garantie/', 'US Link': '/users/dashboard-garantie/'
        },
        
        # EPIC: Archives (P3)
        {
            'Prio': 'P3', 'EPIC': 'Archives', 'Feature': 'Archivage électronique', 
            'Persona': 'Super Admin', 'Macro US': 'En tant qu\'admin, je veux archiver',
            'RG': 'RG-ARC-001: Conservation légale',
            'US': 'US-ARC-001: Archiver les documents',
            'Dépendance': 'Demandes Équipement', 'Statut': 'À faire', 'Commentaire': 'Archivage sécurisé',
            'Feature Link': '/demande_equipement/archives/', 'US Link': '/demande_equipement/archives/'
        },
        
        # EPIC: API (P3)
        {
            'Prio': 'P3', 'EPIC': 'API', 'Feature': 'API REST', 
            'Persona': 'Super Admin', 'Macro US': 'En tant qu\'admin, je veux une API',
            'RG': 'RG-API-001: Documentation OpenAPI',
            'US': 'US-API-001: Exposer les données via API',
            'Dépendance': '-', 'Statut': 'À faire', 'Commentaire': 'API RESTful complète',
            'Feature Link': '/api/', 'US Link': '/api/'
        },
        
        # EPIC: Sécurité (P3)
        {
            'Prio': 'P3', 'EPIC': 'Sécurité', 'Feature': 'Audit des permissions', 
            'Persona': 'Super Admin', 'Macro US': 'En tant qu\'admin, je veux auditer',
            'RG': 'RG-SEC-001: Traçabilité des actions',
            'US': 'US-SEC-001: Voir les logs d\'audit',
            'Dépendance': 'Authentification', 'Statut': 'À faire', 'Commentaire': 'Journalisation complète',
            'Feature Link': '/audit/', 'US Link': '/audit/'
        }
    ]
    
    # Création du DataFrame
    df = pd.DataFrame(backlog_data)
    
    # Nom du fichier avec timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Backlog_Produit_ParcInfo_{timestamp}.xlsx"
    
    # Création du fichier Excel avec formatage
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Backlog Produit', index=False)
        
        # Récupération du workbook et worksheet
        workbook = writer.book
        worksheet = writer.sheets['Backlog Produit']
        
        # Formatage des colonnes
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    print(f"✅ Backlog produit généré avec succès: {filename}")
    print(f"📊 {len(backlog_data)} fonctionnalités documentées")
    print(f"📁 Fichier créé dans: {os.path.abspath(filename)}")
    
    return filename

if __name__ == "__main__":
    create_backlog_excel()
