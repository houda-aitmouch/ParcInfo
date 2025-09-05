#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de Backlog Produit - ParcInfo
Crée un backlog produit structuré avec toutes les fonctionnalités du projet
"""

import pandas as pd
from datetime import datetime
import os

def generate_backlog():
    """Génère le backlog produit complet pour ParcInfo"""
    
    # Données du backlog
    backlog_data = [
        # === AUTHENTIFICATION ET UTILISATEURS ===
        {
            'Prio': 'P1', 'EPIC': 'Authentification', 'Feature': 'Interface de connexion',
            'Persona': 'Employé', 'Macro US': 'En tant qu\'utilisateur, je veux me connecter au système pour accéder à mes fonctionnalités',
            'RG': 'RG-AUTH-001: Champs identifiant et mot de passe obligatoires avec validation',
            'US': 'US-AUTH-001: Saisir mon identifiant et mot de passe pour me connecter',
            'Dépendance': '-', 'Statut': 'Terminé', 'Commentaire': 'Interface responsive avec validation côté client et serveur',
            'Feature Link': '/users/login/', 'US Link': '/users/login/'
        },
        {
            'Prio': 'P1', 'EPIC': 'Authentification', 'Feature': 'Gestion des sessions',
            'Persona': 'Employé', 'Macro US': 'En tant qu\'utilisateur, je veux rester connecté pendant ma session de travail',
            'RG': 'RG-AUTH-002: Session valide pendant 8h d\'inactivité avec renouvellement automatique',
            'US': 'US-AUTH-002: Ma session reste active pendant mon travail avec timeout configurable',
            'Dépendance': 'Interface de connexion', 'Statut': 'Terminé', 'Commentaire': 'Sessions Django avec middleware personnalisé',
            'Feature Link': '/users/logout/', 'US Link': '/users/logout/'
        },
        {
            'Prio': 'P1', 'EPIC': 'Authentification', 'Feature': 'Redirection par rôle',
            'Persona': 'Employé', 'Macro US': 'En tant qu\'utilisateur, je veux être redirigé vers mon dashboard approprié',
            'RG': 'RG-AUTH-003: Redirection automatique selon le groupe utilisateur après connexion',
            'US': 'US-AUTH-003: Accéder directement à mon espace de travail personnalisé',
            'Dépendance': 'Interface de connexion', 'Statut': 'Terminé', 'Commentaire': 'Middleware de redirection par rôle',
            'Feature Link': '/users/redirect-user/', 'US Link': '/users/redirect-user/'
        },
        {
            'Prio': 'P1', 'EPIC': 'Gestion Utilisateurs', 'Feature': 'Profil utilisateur',
            'Persona': 'Employé', 'Macro US': 'En tant qu\'utilisateur, je veux consulter et modifier mon profil',
            'RG': 'RG-USER-001: Données personnelles modifiables avec validation des champs',
            'US': 'US-USER-001: Voir et modifier mes informations personnelles et préférences',
            'Dépendance': 'Authentification', 'Statut': 'Terminé', 'Commentaire': 'Gestion des données personnelles sécurisée',
            'Feature Link': '/users/profil/', 'US Link': '/users/profil/'
        },
        {
            'Prio': 'P1', 'EPIC': 'Gestion Utilisateurs', 'Feature': 'Gestion des rôles',
            'Persona': 'Super Admin', 'Macro US': 'En tant qu\'admin, je veux gérer les rôles et permissions',
            'RG': 'RG-USER-002: 4 rôles distincts avec permissions spécifiques et hiérarchie',
            'US': 'US-USER-002: Créer/modifier les groupes d\'utilisateurs et leurs permissions',
            'Dépendance': 'Authentification', 'Statut': 'Terminé', 'Commentaire': 'Système de groupes Django avec permissions personnalisées',
            'Feature Link': '/users/superadmin/', 'US Link': '/users/superadmin/'
        },
        
        # === DEMANDES D'ÉQUIPEMENT ===
        {
            'Prio': 'P1', 'EPIC': 'Demandes Équipement', 'Feature': 'Création de demande',
            'Persona': 'Employé', 'Macro US': 'En tant qu\'employé, je veux créer une demande d\'équipement',
            'RG': 'RG-DEM-001: Champs obligatoires selon le type (informatique/bureau) avec validation',
            'US': 'US-DEM-001: Remplir le formulaire de demande avec sélection du matériel',
            'Dépendance': 'Authentification', 'Statut': 'Terminé', 'Commentaire': 'Formulaire dynamique selon catégorie avec validation',
            'Feature Link': '/demande_equipement/nouvelle/', 'US Link': '/demande_equipement/nouvelle/'
        },
        {
            'Prio': 'P1', 'EPIC': 'Demandes Équipement', 'Feature': 'Consultation des demandes',
            'Persona': 'Employé', 'Macro US': 'En tant qu\'employé, je veux voir mes demandes et leur statut',
            'RG': 'RG-DEM-002: Seules mes demandes visibles avec filtrage par statut et date',
            'US': 'US-DEM-002: Lister mes demandes avec statuts et dates de traitement',
            'Dépendance': 'Création de demande', 'Statut': 'Terminé', 'Commentaire': 'Interface de consultation avec filtres avancés',
            'Feature Link': '/demande_equipement/', 'US Link': '/demande_equipement/'
        },
        {
            'Prio': 'P1', 'EPIC': 'Demandes Équipement', 'Feature': 'Approbation des demandes',
            'Persona': 'Gestionnaire Info', 'Macro US': 'En tant que gestionnaire, je veux approuver/rejeter les demandes',
            'RG': 'RG-DEM-003: Validation selon budget, disponibilité et politique d\'entreprise',
            'US': 'US-DEM-003: Traiter les demandes en attente avec commentaires de validation',
            'Dépendance': 'Création de demande', 'Statut': 'Terminé', 'Commentaire': 'Workflow d\'approbation avec notifications',
            'Feature Link': '/demande_equipement/approuver/<id>/', 'US Link': '/demande_equipement/approuver/<id>/'
        },
        {
            'Prio': 'P1', 'EPIC': 'Demandes Équipement', 'Feature': 'Signature de décharge',
            'Persona': 'Employé', 'Macro US': 'En tant qu\'employé, je veux signer ma décharge électroniquement',
            'RG': 'RG-DEM-004: Signature obligatoire avant réception avec horodatage',
            'US': 'US-DEM-004: Signer électroniquement ma décharge pour recevoir l\'équipement',
            'Dépendance': 'Approbation de demande', 'Statut': 'Terminé', 'Commentaire': 'Signature électronique sécurisée avec PDF',
            'Feature Link': '/demande_equipement/signer-decharge/<id>/', 'US Link': '/demande_equipement/signer-decharge/<id>/'
        },
        
        # === MATÉRIEL INFORMATIQUE ===
        {
            'Prio': 'P1', 'EPIC': 'Matériel Informatique', 'Feature': 'Gestion du parc',
            'Persona': 'Gestionnaire Info', 'Macro US': 'En tant que gestionnaire, je veux gérer le matériel informatique',
            'RG': 'RG-MAT-001: Inventaire complet avec codes uniques et traçabilité',
            'US': 'US-MAT-001: Ajouter/modifier/supprimer du matériel avec codes d\'inventaire',
            'Dépendance': '-', 'Statut': 'Terminé', 'Commentaire': 'Codes d\'inventaire automatiques avec QR codes',
            'Feature Link': '/materiel_informatique/', 'US Link': '/materiel_informatique/'
        },
        {
            'Prio': 'P1', 'EPIC': 'Matériel Informatique', 'Feature': 'Affectation d\'équipements',
            'Persona': 'Gestionnaire Info', 'Macro US': 'En tant que gestionnaire, je veux affecter des équipements',
            'RG': 'RG-MAT-002: Un équipement par utilisateur maximum avec historique des affectations',
            'US': 'US-MAT-002: Assigner un équipement à un utilisateur avec date d\'affectation',
            'Dépendance': 'Gestion du parc', 'Statut': 'Terminé', 'Commentaire': 'Traçabilité complète des affectations',
            'Feature Link': '/materiel_informatique/affecter/', 'US Link': '/materiel_informatique/affecter/'
        },
        
        # === MATÉRIEL BUREAU ===
        {
            'Prio': 'P1', 'EPIC': 'Matériel Bureau', 'Feature': 'Gestion du mobilier',
            'Persona': 'Gestionnaire Bureau', 'Macro US': 'En tant que gestionnaire bureau, je veux gérer le mobilier',
            'RG': 'RG-MAT-003: Inventaire bureau avec localisation et état du mobilier',
            'US': 'US-MAT-003: Gérer le mobilier de bureau avec affectation par espace',
            'Dépendance': '-', 'Statut': 'Terminé', 'Commentaire': 'Gestion des espaces de travail et mobilier',
            'Feature Link': '/materiel_bureautique/', 'US Link': '/materiel_bureautique/'
        },
        {
            'Prio': 'P1', 'EPIC': 'Matériel Bureau', 'Feature': 'Affectation mobilier',
            'Persona': 'Gestionnaire Bureau', 'Macro US': 'En tant que gestionnaire bureau, je veux affecter du mobilier',
            'RG': 'RG-MAT-004: Mobilier selon poste de travail et ergonomie',
            'US': 'US-MAT-004: Assigner du mobilier aux employés selon leur poste',
            'Dépendance': 'Gestion du mobilier', 'Statut': 'Terminé', 'Commentaire': 'Configuration poste de travail optimisée',
            'Feature Link': '/materiel_bureautique/affecter/', 'US Link': '/materiel_bureautique/affecter/'
        },
        
        # === COMMANDES INFORMATIQUES ===
        {
            'Prio': 'P1', 'EPIC': 'Commandes Informatiques', 'Feature': 'Création de commande',
            'Persona': 'Gestionnaire Info', 'Macro US': 'En tant que gestionnaire, je veux créer des commandes informatiques',
            'RG': 'RG-COM-001: Validation fournisseur et budget avec approbation hiérarchique',
            'US': 'US-COM-001: Créer une commande avec lignes détaillées et devis',
            'Dépendance': 'Gestion du parc', 'Statut': 'Terminé', 'Commentaire': 'Gestion des devis et budgets avec validation',
            'Feature Link': '/commande_informatique/ajouter/', 'US Link': '/commande_informatique/ajouter/'
        },
        {
            'Prio': 'P1', 'EPIC': 'Commandes Informatiques', 'Feature': 'Suivi des commandes',
            'Persona': 'Gestionnaire Info', 'Macro US': 'En tant que gestionnaire, je veux suivre mes commandes',
            'RG': 'RG-COM-002: Statuts de commande obligatoires avec notifications de progression',
            'US': 'US-COM-002: Voir l\'état de mes commandes avec dates de livraison',
            'Dépendance': 'Création de commande', 'Statut': 'Terminé', 'Commentaire': 'Workflow de commande avec suivi temps réel',
            'Feature Link': '/commande_informatique/liste/', 'US Link': '/commande_informatique/liste/'
        },
        
        # === COMMANDES BUREAU ===
        {
            'Prio': 'P1', 'EPIC': 'Commandes Bureau', 'Feature': 'Création commande bureau',
            'Persona': 'Gestionnaire Bureau', 'Macro US': 'En tant que gestionnaire bureau, je veux commander du mobilier',
            'RG': 'RG-COM-003: Validation fournisseur bureau avec catalogue produits',
            'US': 'US-COM-003: Créer commande mobilier avec sélection catalogue',
            'Dépendance': 'Gestion du mobilier', 'Statut': 'Terminé', 'Commentaire': 'Catalogue fournisseurs bureau intégré',
            'Feature Link': '/commande_bureau/ajouter/', 'US Link': '/commande_bureau/ajouter/'
        },
        {
            'Prio': 'P1', 'EPIC': 'Commandes Bureau', 'Feature': 'Suivi commandes bureau',
            'Persona': 'Gestionnaire Bureau', 'Macro US': 'En tant que gestionnaire bureau, je veux suivre mes commandes',
            'RG': 'RG-COM-004: Statuts spécifiques bureau avec gestion des délais',
            'US': 'US-COM-004: Suivre commandes mobilier avec alertes de retard',
            'Dépendance': 'Création commande bureau', 'Statut': 'Terminé', 'Commentaire': 'Gestion des délais livraison avec alertes',
            'Feature Link': '/commande_bureau/liste/', 'US Link': '/commande_bureau/liste/'
        },
        
        # === FOURNISSEURS ===
        {
            'Prio': 'P1', 'EPIC': 'Fournisseurs', 'Feature': 'Gestion catalogue',
            'Persona': 'Super Admin', 'Macro US': 'En tant qu\'admin, je veux gérer les fournisseurs',
            'RG': 'RG-FOU-001: Données fournisseur complètes avec contacts et devis',
            'US': 'US-FOU-001: Ajouter/modifier fournisseurs avec informations complètes',
            'Dépendance': '-', 'Statut': 'Terminé', 'Commentaire': 'Base de données fournisseurs avec historique',
            'Feature Link': '/fournisseurs/', 'US Link': '/fournisseurs/'
        },
        {
            'Prio': 'P1', 'EPIC': 'Fournisseurs', 'Feature': 'Catalogue produits',
            'Persona': 'Super Admin', 'Macro US': 'En tant qu\'admin, je veux gérer les catalogues',
            'RG': 'RG-FOU-002: Désignations et descriptions standardisées par catégorie',
            'US': 'US-FOU-002: Maintenir les catalogues produits avec prix et disponibilité',
            'Dépendance': 'Gestion catalogue', 'Statut': 'Terminé', 'Commentaire': 'Classification produits avec taxonomie',
            'Feature Link': '/fournisseurs/catalogue/', 'US Link': '/fournisseurs/catalogue/'
        },
        
        # === LIVRAISONS ===
        {
            'Prio': 'P1', 'EPIC': 'Livraisons', 'Feature': 'Réception de livraisons',
            'Persona': 'Gestionnaire Info', 'Macro US': 'En tant que gestionnaire, je veux réceptionner les livraisons',
            'RG': 'RG-LIV-001: PV de réception obligatoire avec contrôle qualité',
            'US': 'US-LIV-001: Valider les livraisons reçues avec signature électronique',
            'Dépendance': 'Commandes', 'Statut': 'Terminé', 'Commentaire': 'Contrôle qualité réception avec photos',
            'Feature Link': '/livraison/nouvelle/', 'US Link': '/livraison/nouvelle/'
        },
        {
            'Prio': 'P1', 'EPIC': 'Livraisons', 'Feature': 'Suivi des livraisons',
            'Persona': 'Gestionnaire Info', 'Macro US': 'En tant que gestionnaire, je veux suivre les livraisons',
            'RG': 'RG-LIV-002: Statuts de livraison avec notifications de progression',
            'US': 'US-LIV-002: Voir l\'état des livraisons avec dates et statuts',
            'Dépendance': 'Réception de livraisons', 'Statut': 'Terminé', 'Commentaire': 'Traçabilité complète avec historique',
            'Feature Link': '/livraison/', 'US Link': '/livraison/'
        },
        
        # === NOTIFICATIONS ===
        {
            'Prio': 'P2', 'EPIC': 'Notifications', 'Feature': 'Système de notifications',
            'Persona': 'Employé', 'Macro US': 'En tant qu\'utilisateur, je veux recevoir des notifications',
            'RG': 'RG-NOT-001: Notifications temps réel avec priorité et catégorisation',
            'US': 'US-NOT-001: Voir mes notifications avec marquage lu/non lu',
            'Dépendance': 'Demandes Équipement', 'Statut': 'Terminé', 'Commentaire': 'Notifications push et email avec templates',
            'Feature Link': '/users/notifications-demandes/', 'US Link': '/users/notifications-demandes/'
        },
        {
            'Prio': 'P2', 'EPIC': 'Notifications', 'Feature': 'Notifications garantie',
            'Persona': 'Employé', 'Macro US': 'En tant qu\'utilisateur, je veux être alerté des garanties',
            'RG': 'RG-NOT-002: Alertes 30 jours avant expiration avec escalade',
            'US': 'US-NOT-002: Recevoir alertes garantie avec actions recommandées',
            'Dépendance': 'Matériel Informatique', 'Statut': 'En cours', 'Commentaire': 'Système d\'alertes automatiques avec dashboard',
            'Feature Link': '/users/notifications-garantie/', 'US Link': '/users/notifications-garantie/'
        },
        
        # === DASHBOARDS ===
        {
            'Prio': 'P2', 'EPIC': 'Dashboard', 'Feature': 'Tableau de bord employé',
            'Persona': 'Employé', 'Macro US': 'En tant qu\'employé, je veux voir mon dashboard',
            'RG': 'RG-DASH-001: Données personnalisées par rôle avec métriques pertinentes',
            'US': 'US-DASH-001: Accéder à mon tableau de bord avec mes équipements et demandes',
            'Dépendance': 'Authentification', 'Statut': 'Terminé', 'Commentaire': 'Vue d\'ensemble personnalisée par utilisateur',
            'Feature Link': '/users/employe/', 'US Link': '/users/employe/'
        },
        {
            'Prio': 'P2', 'EPIC': 'Dashboard', 'Feature': 'Dashboard gestionnaire info',
            'Persona': 'Gestionnaire Info', 'Macro US': 'En tant que gestionnaire, je veux mon dashboard',
            'RG': 'RG-DASH-002: Métriques informatiques avec KPIs et alertes',
            'US': 'US-DASH-002: Voir les KPIs informatiques et demandes en attente',
            'Dépendance': 'Authentification', 'Statut': 'Terminé', 'Commentaire': 'Indicateurs de performance avec graphiques',
            'Feature Link': '/users/gestionnaire_info/', 'US Link': '/users/gestionnaire_info/'
        },
        {
            'Prio': 'P2', 'EPIC': 'Dashboard', 'Feature': 'Dashboard gestionnaire bureau',
            'Persona': 'Gestionnaire Bureau', 'Macro US': 'En tant que gestionnaire bureau, je veux mon dashboard',
            'RG': 'RG-DASH-003: Métriques bureau avec inventaire et commandes',
            'US': 'US-DASH-003: Voir les KPIs bureau et mobilier disponible',
            'Dépendance': 'Authentification', 'Statut': 'Terminé', 'Commentaire': 'Indicateurs bureau avec gestion d\'espace',
            'Feature Link': '/users/gestionnaire_bureau/', 'US Link': '/users/gestionnaire_bureau/'
        },
        {
            'Prio': 'P2', 'EPIC': 'Dashboard', 'Feature': 'Dashboard super admin',
            'Persona': 'Super Admin', 'Macro US': 'En tant qu\'admin, je veux le dashboard complet',
            'RG': 'RG-DASH-004: Vue globale du système avec toutes les métriques',
            'US': 'US-DASH-004: Accéder à toutes les données et configurations système',
            'Dépendance': 'Authentification', 'Statut': 'Terminé', 'Commentaire': 'Administration complète avec monitoring',
            'Feature Link': '/users/superadmin/', 'US Link': '/users/superadmin/'
        },
        
        # === CHATBOT ===
        {
            'Prio': 'P2', 'EPIC': 'Chatbot', 'Feature': 'Assistant IA',
            'Persona': 'Employé', 'Macro US': 'En tant qu\'utilisateur, je veux poser des questions',
            'RG': 'RG-CHAT-001: Réponses basées sur la base de connaissances avec RAG',
            'US': 'US-CHAT-001: Interroger l\'assistant IA pour obtenir de l\'aide',
            'Dépendance': '-', 'Statut': 'Terminé', 'Commentaire': 'RAG avec base de connaissances intégrée',
            'Feature Link': '/chatbot/', 'US Link': '/chatbot/'
        },
        {
            'Prio': 'P2', 'EPIC': 'Chatbot', 'Feature': 'Base de connaissances',
            'Persona': 'Super Admin', 'Macro US': 'En tant qu\'admin, je veux maintenir la base',
            'RG': 'RG-CHAT-002: Documentation à jour avec indexation vectorielle',
            'US': 'US-CHAT-002: Mettre à jour la documentation et les réponses du chatbot',
            'Dépendance': 'Assistant IA', 'Statut': 'Terminé', 'Commentaire': 'Système RAG avancé avec apprentissage continu',
            'Feature Link': '/chatbot/admin/', 'US Link': '/chatbot/admin/'
        },
        
        # === RAPPORTS ===
        {
            'Prio': 'P2', 'EPIC': 'Rapports', 'Feature': 'Export Excel',
            'Persona': 'Gestionnaire Info', 'Macro US': 'En tant que gestionnaire, je veux exporter des données',
            'RG': 'RG-RAP-001: Formats Excel standardisés avec templates personnalisés',
            'US': 'US-RAP-001: Exporter les données en Excel avec graphiques et tableaux',
            'Dépendance': 'Gestion du parc', 'Statut': 'Terminé', 'Commentaire': 'Templates Excel personnalisés par module',
            'Feature Link': '/materiel_informatique/export_excel/', 'US Link': '/materiel_informatique/export_excel/'
        },
        {
            'Prio': 'P2', 'EPIC': 'Rapports', 'Feature': 'Rapports de livraison',
            'Persona': 'Gestionnaire Info', 'Macro US': 'En tant que gestionnaire, je veux des rapports',
            'RG': 'RG-RAP-002: Statistiques de livraison avec analyse des délais',
            'US': 'US-RAP-002: Générer des rapports de performance des fournisseurs',
            'Dépendance': 'Livraisons', 'Statut': 'En cours', 'Commentaire': 'Tableaux de bord analytiques avec graphiques',
            'Feature Link': '/livraison/rapports/', 'US Link': '/livraison/rapports/'
        },
        
        # === RECHERCHE ===
        {
            'Prio': 'P2', 'EPIC': 'Recherche', 'Feature': 'Recherche globale',
            'Persona': 'Employé', 'Macro US': 'En tant qu\'utilisateur, je veux rechercher',
            'RG': 'RG-RECH-001: Recherche multi-critères avec filtres avancés',
            'US': 'US-RECH-001: Trouver rapidement des informations dans le système',
            'Dépendance': '-', 'Statut': 'À faire', 'Commentaire': 'Recherche sémantique avec autocomplétion',
            'Feature Link': '/users/search/', 'US Link': '/users/search/'
        },
        
        # === GARANTIES ===
        {
            'Prio': 'P3', 'EPIC': 'Garanties', 'Feature': 'Suivi des garanties',
            'Persona': 'Gestionnaire Info', 'Macro US': 'En tant que gestionnaire, je veux suivre les garanties',
            'RG': 'RG-GAR-001: Alertes automatiques avec gestion des renouvellements',
            'US': 'US-GAR-001: Gérer les garanties avec notifications d\'expiration',
            'Dépendance': 'Matériel Informatique', 'Statut': 'En cours', 'Commentaire': 'Système d\'alertes avec dashboard dédié',
            'Feature Link': '/users/dashboard-garantie/', 'US Link': '/users/dashboard-garantie/'
        },
        
        # === ARCHIVES ===
        {
            'Prio': 'P3', 'EPIC': 'Archives', 'Feature': 'Archivage électronique',
            'Persona': 'Super Admin', 'Macro US': 'En tant qu\'admin, je veux archiver',
            'RG': 'RG-ARC-001: Conservation légale avec indexation et recherche',
            'US': 'US-ARC-001: Archiver les documents selon la politique de rétention',
            'Dépendance': 'Demandes Équipement', 'Statut': 'À faire', 'Commentaire': 'Archivage sécurisé avec compression',
            'Feature Link': '/demande_equipement/archives/', 'US Link': '/demande_equipement/archives/'
        },
        
        # === API ===
        {
            'Prio': 'P3', 'EPIC': 'API', 'Feature': 'API REST',
            'Persona': 'Super Admin', 'Macro US': 'En tant qu\'admin, je veux une API',
            'RG': 'RG-API-001: Documentation OpenAPI avec authentification OAuth2',
            'US': 'US-API-001: Exposer les données via API RESTful sécurisée',
            'Dépendance': '-', 'Statut': 'À faire', 'Commentaire': 'API RESTful complète avec documentation interactive',
            'Feature Link': '/api/', 'US Link': '/api/'
        },
        
        # === SÉCURITÉ ===
        {
            'Prio': 'P3', 'EPIC': 'Sécurité', 'Feature': 'Audit des permissions',
            'Persona': 'Super Admin', 'Macro US': 'En tant qu\'admin, je veux auditer',
            'RG': 'RG-SEC-001: Traçabilité des actions avec logs détaillés',
            'US': 'US-SEC-001: Voir les logs d\'audit et les actions des utilisateurs',
            'Dépendance': 'Authentification', 'Statut': 'À faire', 'Commentaire': 'Journalisation complète avec alertes sécurité',
            'Feature Link': '/audit/', 'US Link': '/audit/'
        },
        
        # === FONCTIONNALITÉS AVANCÉES ===
        {
            'Prio': 'P3', 'EPIC': 'Mobile', 'Feature': 'Application mobile',
            'Persona': 'Employé', 'Macro US': 'En tant qu\'utilisateur, je veux accéder depuis mobile',
            'RG': 'RG-MOB-001: Interface responsive avec fonctionnalités essentielles',
            'US': 'US-MOB-001: Consulter mes demandes et équipements depuis mobile',
            'Dépendance': 'API REST', 'Statut': 'À faire', 'Commentaire': 'Application mobile native ou PWA',
            'Feature Link': '/mobile/', 'US Link': '/mobile/'
        },
        {
            'Prio': 'P3', 'EPIC': 'Intégration', 'Feature': 'Intégration RH',
            'Persona': 'Super Admin', 'Macro US': 'En tant qu\'admin, je veux intégrer avec les RH',
            'RG': 'RG-INT-001: Synchronisation automatique des utilisateurs',
            'US': 'US-INT-001: Importer les utilisateurs depuis le système RH',
            'Dépendance': 'API REST', 'Statut': 'À faire', 'Commentaire': 'Intégration LDAP/Active Directory',
            'Feature Link': '/integration/rh/', 'US Link': '/integration/rh/'
        },
        {
            'Prio': 'P3', 'EPIC': 'BI', 'Feature': 'Business Intelligence',
            'Persona': 'Super Admin', 'Macro US': 'En tant qu\'admin, je veux des analyses avancées',
            'RG': 'RG-BI-001: Tableaux de bord interactifs avec drill-down',
            'US': 'US-BI-001: Analyser les tendances et optimiser les processus',
            'Dépendance': 'Rapports', 'Statut': 'À faire', 'Commentaire': 'Intégration Power BI ou Tableau',
            'Feature Link': '/bi/', 'US Link': '/bi/'
        }
    ]
    
    # Création du DataFrame
    df = pd.DataFrame(backlog_data)
    
    # Tri par priorité et EPIC
    priority_order = {'P1': 1, 'P2': 2, 'P3': 3}
    df['Prio_Order'] = df['Prio'].map(priority_order)
    df = df.sort_values(['Prio_Order', 'EPIC', 'Feature'])
    df = df.drop('Prio_Order', axis=1)
    
    # Génération du fichier Excel
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Backlog_Produit_ParcInfo_{timestamp}.xlsx"
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Feuille principale
        df.to_excel(writer, sheet_name='Backlog Produit', index=False)
        
        # Feuille des personas
        personas_data = [
            {
                'Persona': 'Employé',
                'Rôle': 'Utilisateur final du système',
                'Responsabilités': 'Créer des demandes, signer des décharges, consulter ses équipements',
                'Accès': 'Dashboard employé, demandes personnelles, notifications',
                'Permissions': 'Lecture sur ses données, écriture sur ses demandes'
            },
            {
                'Persona': 'Gestionnaire Informatique',
                'Rôle': 'Gestionnaire du parc informatique',
                'Responsabilités': 'Approuver demandes IT, gérer matériel informatique, suivre commandes IT',
                'Accès': 'Dashboard gestionnaire info, matériel informatique, commandes IT',
                'Permissions': 'Lecture/écriture sur matériel IT, approbation demandes IT'
            },
            {
                'Persona': 'Gestionnaire Bureau',
                'Rôle': 'Gestionnaire du mobilier et fournitures de bureau',
                'Responsabilités': 'Approuver demandes bureau, gérer mobilier, suivre commandes bureau',
                'Accès': 'Dashboard gestionnaire bureau, matériel bureau, commandes bureau',
                'Permissions': 'Lecture/écriture sur matériel bureau, approbation demandes bureau'
            },
            {
                'Persona': 'Super Admin',
                'Rôle': 'Administrateur système',
                'Responsabilités': 'Gestion complète du système, utilisateurs, fournisseurs',
                'Accès': 'Toutes les fonctionnalités, configuration système',
                'Permissions': 'Accès complet à toutes les fonctionnalités'
            }
        ]
        
        personas_df = pd.DataFrame(personas_data)
        personas_df.to_excel(writer, sheet_name='Personas', index=False)
        
        # Feuille des EPICs
        epics_data = [
            {'EPIC': 'Authentification', 'Description': 'Gestion des connexions et sessions utilisateurs', 'Responsable': 'Super Admin'},
            {'EPIC': 'Gestion Utilisateurs', 'Description': 'Gestion des profils et rôles utilisateurs', 'Responsable': 'Super Admin'},
            {'EPIC': 'Demandes Équipement', 'Description': 'Workflow de demandes d\'équipement', 'Responsable': 'Gestionnaire Info/Bureau'},
            {'EPIC': 'Matériel Informatique', 'Description': 'Gestion du parc informatique', 'Responsable': 'Gestionnaire Info'},
            {'EPIC': 'Matériel Bureau', 'Description': 'Gestion du mobilier et fournitures', 'Responsable': 'Gestionnaire Bureau'},
            {'EPIC': 'Commandes Informatiques', 'Description': 'Gestion des commandes informatiques', 'Responsable': 'Gestionnaire Info'},
            {'EPIC': 'Commandes Bureau', 'Description': 'Gestion des commandes bureau', 'Responsable': 'Gestionnaire Bureau'},
            {'EPIC': 'Fournisseurs', 'Description': 'Gestion des fournisseurs et catalogues', 'Responsable': 'Super Admin'},
            {'EPIC': 'Livraisons', 'Description': 'Suivi des livraisons et réceptions', 'Responsable': 'Gestionnaire Info'},
            {'EPIC': 'Notifications', 'Description': 'Système de notifications et alertes', 'Responsable': 'Super Admin'},
            {'EPIC': 'Dashboard', 'Description': 'Tableaux de bord personnalisés', 'Responsable': 'Super Admin'},
            {'EPIC': 'Chatbot', 'Description': 'Assistant IA et base de connaissances', 'Responsable': 'Super Admin'},
            {'EPIC': 'Rapports', 'Description': 'Génération de rapports et exports', 'Responsable': 'Gestionnaire Info'},
            {'EPIC': 'Recherche', 'Description': 'Recherche globale et filtres', 'Responsable': 'Super Admin'},
            {'EPIC': 'Garanties', 'Description': 'Suivi des garanties et alertes', 'Responsable': 'Gestionnaire Info'},
            {'EPIC': 'Archives', 'Description': 'Archivage électronique sécurisé', 'Responsable': 'Super Admin'},
            {'EPIC': 'API', 'Description': 'API REST pour intégrations', 'Responsable': 'Super Admin'},
            {'EPIC': 'Sécurité', 'Description': 'Audit et sécurité du système', 'Responsable': 'Super Admin'},
            {'EPIC': 'Mobile', 'Description': 'Application mobile et PWA', 'Responsable': 'Super Admin'},
            {'EPIC': 'Intégration', 'Description': 'Intégrations avec systèmes externes', 'Responsable': 'Super Admin'},
            {'EPIC': 'BI', 'Description': 'Business Intelligence et analytics', 'Responsable': 'Super Admin'}
        ]
        
        epics_df = pd.DataFrame(epics_data)
        epics_df.to_excel(writer, sheet_name='EPICs', index=False)
        
        # Feuille des règles de gestion
        rg_data = [
            {'RG': 'RG-AUTH-001', 'Description': 'Champs identifiant et mot de passe obligatoires avec validation', 'EPIC': 'Authentification'},
            {'RG': 'RG-AUTH-002', 'Description': 'Session valide pendant 8h d\'inactivité avec renouvellement automatique', 'EPIC': 'Authentification'},
            {'RG': 'RG-AUTH-003', 'Description': 'Redirection automatique selon le groupe utilisateur après connexion', 'EPIC': 'Authentification'},
            {'RG': 'RG-USER-001', 'Description': 'Données personnelles modifiables avec validation des champs', 'EPIC': 'Gestion Utilisateurs'},
            {'RG': 'RG-USER-002', 'Description': '4 rôles distincts avec permissions spécifiques et hiérarchie', 'EPIC': 'Gestion Utilisateurs'},
            {'RG': 'RG-DEM-001', 'Description': 'Champs obligatoires selon le type (informatique/bureau) avec validation', 'EPIC': 'Demandes Équipement'},
            {'RG': 'RG-DEM-002', 'Description': 'Seules mes demandes visibles avec filtrage par statut et date', 'EPIC': 'Demandes Équipement'},
            {'RG': 'RG-DEM-003', 'Description': 'Validation selon budget, disponibilité et politique d\'entreprise', 'EPIC': 'Demandes Équipement'},
            {'RG': 'RG-DEM-004', 'Description': 'Signature obligatoire avant réception avec horodatage', 'EPIC': 'Demandes Équipement'},
            {'RG': 'RG-MAT-001', 'Description': 'Inventaire complet avec codes uniques et traçabilité', 'EPIC': 'Matériel Informatique'},
            {'RG': 'RG-MAT-002', 'Description': 'Un équipement par utilisateur maximum avec historique des affectations', 'EPIC': 'Matériel Informatique'},
            {'RG': 'RG-MAT-003', 'Description': 'Inventaire bureau avec localisation et état du mobilier', 'EPIC': 'Matériel Bureau'},
            {'RG': 'RG-MAT-004', 'Description': 'Mobilier selon poste de travail et ergonomie', 'EPIC': 'Matériel Bureau'},
            {'RG': 'RG-COM-001', 'Description': 'Validation fournisseur et budget avec approbation hiérarchique', 'EPIC': 'Commandes Informatiques'},
            {'RG': 'RG-COM-002', 'Description': 'Statuts de commande obligatoires avec notifications de progression', 'EPIC': 'Commandes Informatiques'},
            {'RG': 'RG-COM-003', 'Description': 'Validation fournisseur bureau avec catalogue produits', 'EPIC': 'Commandes Bureau'},
            {'RG': 'RG-COM-004', 'Description': 'Statuts spécifiques bureau avec gestion des délais', 'EPIC': 'Commandes Bureau'},
            {'RG': 'RG-FOU-001', 'Description': 'Données fournisseur complètes avec contacts et devis', 'EPIC': 'Fournisseurs'},
            {'RG': 'RG-FOU-002', 'Description': 'Désignations et descriptions standardisées par catégorie', 'EPIC': 'Fournisseurs'},
            {'RG': 'RG-LIV-001', 'Description': 'PV de réception obligatoire avec contrôle qualité', 'EPIC': 'Livraisons'},
            {'RG': 'RG-LIV-002', 'Description': 'Statuts de livraison avec notifications de progression', 'EPIC': 'Livraisons'},
            {'RG': 'RG-NOT-001', 'Description': 'Notifications temps réel avec priorité et catégorisation', 'EPIC': 'Notifications'},
            {'RG': 'RG-NOT-002', 'Description': 'Alertes 30 jours avant expiration avec escalade', 'EPIC': 'Notifications'},
            {'RG': 'RG-DASH-001', 'Description': 'Données personnalisées par rôle avec métriques pertinentes', 'EPIC': 'Dashboard'},
            {'RG': 'RG-DASH-002', 'Description': 'Métriques informatiques avec KPIs et alertes', 'EPIC': 'Dashboard'},
            {'RG': 'RG-DASH-003', 'Description': 'Métriques bureau avec inventaire et commandes', 'EPIC': 'Dashboard'},
            {'RG': 'RG-DASH-004', 'Description': 'Vue globale du système avec toutes les métriques', 'EPIC': 'Dashboard'},
            {'RG': 'RG-CHAT-001', 'Description': 'Réponses basées sur la base de connaissances avec RAG', 'EPIC': 'Chatbot'},
            {'RG': 'RG-CHAT-002', 'Description': 'Documentation à jour avec indexation vectorielle', 'EPIC': 'Chatbot'},
            {'RG': 'RG-RAP-001', 'Description': 'Formats Excel standardisés avec templates personnalisés', 'EPIC': 'Rapports'},
            {'RG': 'RG-RAP-002', 'Description': 'Statistiques de livraison avec analyse des délais', 'EPIC': 'Rapports'},
            {'RG': 'RG-RECH-001', 'Description': 'Recherche multi-critères avec filtres avancés', 'EPIC': 'Recherche'},
            {'RG': 'RG-GAR-001', 'Description': 'Alertes automatiques avec gestion des renouvellements', 'EPIC': 'Garanties'},
            {'RG': 'RG-ARC-001', 'Description': 'Conservation légale avec indexation et recherche', 'EPIC': 'Archives'},
            {'RG': 'RG-API-001', 'Description': 'Documentation OpenAPI avec authentification OAuth2', 'EPIC': 'API'},
            {'RG': 'RG-SEC-001', 'Description': 'Traçabilité des actions avec logs détaillés', 'EPIC': 'Sécurité'},
            {'RG': 'RG-MOB-001', 'Description': 'Interface responsive avec fonctionnalités essentielles', 'EPIC': 'Mobile'},
            {'RG': 'RG-INT-001', 'Description': 'Synchronisation automatique des utilisateurs', 'EPIC': 'Intégration'},
            {'RG': 'RG-BI-001', 'Description': 'Tableaux de bord interactifs avec drill-down', 'EPIC': 'BI'}
        ]
        
        rg_df = pd.DataFrame(rg_data)
        rg_df.to_excel(writer, sheet_name='Règles de Gestion', index=False)
    
    print(f"✅ Backlog produit généré : {filename}")
    print(f"📊 {len(df)} fonctionnalités organisées en {len(df['EPIC'].unique())} EPICs")
    print(f"👥 {len(df['Persona'].unique())} personas identifiés")
    print(f"📋 {len(rg_data)} règles de gestion définies")
    
    return filename

if __name__ == "__main__":
    generate_backlog()
