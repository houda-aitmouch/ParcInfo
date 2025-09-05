# 📋 Backlog Produit - ParcInfo

## 🎯 Vue d'Ensemble
Ce backlog définit les fonctionnalités du système de gestion de parc informatique ParcInfo, organisées par EPIC et priorisées selon les besoins métier.

---

## 📊 Tableau du Backlog

| Prio | EPIC | Feature | Persona | Macro US | RG | US | Dépendance | Statut | Commentaire | Feature Link | US Link |
|------|------|---------|---------|----------|----|----|------------|--------|-------------|--------------|---------|
| P1 | Authentification | Interface de connexion | Employé | En tant qu'utilisateur, je veux me connecter au système pour accéder à mes fonctionnalités | RG-AUTH-001: Champs identifiant et mot de passe obligatoires | US-AUTH-001: Saisir mon identifiant et mot de passe pour me connecter | - | À faire | Interface responsive et sécurisée | `/users/login/` | `/users/login/` |
| P1 | Authentification | Gestion des sessions | Employé | En tant qu'utilisateur, je veux rester connecté pendant ma session de travail | RG-AUTH-002: Session valide pendant 8h d'inactivité | US-AUTH-002: Ma session reste active pendant mon travail | - | À faire | Timeout configurable | `/users/logout/` | `/users/logout/` |
| P1 | Authentification | Redirection par rôle | Employé | En tant qu'utilisateur, je veux être redirigé vers mon dashboard approprié | RG-AUTH-003: Redirection selon le groupe utilisateur | US-AUTH-003: Accéder directement à mon espace de travail | - | À faire | Dashboard personnalisé par rôle | `/users/redirect-user/` | `/users/redirect-user/` |
| P1 | Gestion Utilisateurs | Profil utilisateur | Employé | En tant qu'utilisateur, je veux consulter et modifier mon profil | RG-USER-001: Données personnelles modifiables | US-USER-001: Voir mes informations personnelles | Authentification | À faire | Gestion des données personnelles | `/users/profil/` | `/users/profil/` |
| P1 | Gestion Utilisateurs | Gestion des rôles | Super Admin | En tant qu'admin, je veux gérer les rôles et permissions | RG-USER-002: 4 rôles distincts avec permissions spécifiques | US-USER-002: Créer/modifier les groupes d'utilisateurs | Authentification | À faire | Rôles: Employé, Gestionnaire Info, Gestionnaire Bureau, Super Admin | `/users/superadmin/` | `/users/superadmin/` |
| P1 | Demandes Équipement | Création de demande | Employé | En tant qu'employé, je veux créer une demande d'équipement | RG-DEM-001: Champs obligatoires selon le type | US-DEM-001: Remplir le formulaire de demande | Authentification | À faire | Formulaire dynamique selon catégorie | `/demande_equipement/nouvelle/` | `/demande_equipement/nouvelle/` |
| P1 | Demandes Équipement | Consultation des demandes | Employé | En tant qu'employé, je veux voir mes demandes | RG-DEM-002: Seules mes demandes visibles | US-DEM-002: Lister mes demandes avec statuts | Authentification | À faire | Filtrage par statut et date | `/demande_equipement/` | `/demande_equipement/` |
| P1 | Demandes Équipement | Approbation des demandes | Gestionnaire Info | En tant que gestionnaire, je veux approuver/rejeter les demandes | RG-DEM-003: Validation selon budget et disponibilité | US-DEM-003: Traiter les demandes en attente | Création de demande | À faire | Workflow d'approbation | `/demande_equipement/approuver/<id>/` | `/demande_equipement/approuver/<id>/` |
| P1 | Demandes Équipement | Signature de décharge | Employé | En tant qu'employé, je veux signer ma décharge | RG-DEM-004: Signature obligatoire avant réception | US-DEM-004: Signer électroniquement ma décharge | Approbation de demande | À faire | Signature électronique sécurisée | `/demande_equipement/signer-decharge/<id>/` | `/demande_equipement/signer-decharge/<id>/` |
| P1 | Matériel Informatique | Gestion du parc | Gestionnaire Info | En tant que gestionnaire, je veux gérer le matériel informatique | RG-MAT-001: Inventaire complet avec codes uniques | US-MAT-001: Ajouter/modifier/supprimer du matériel | - | À faire | Codes d'inventaire automatiques | `/materiel_informatique/` | `/materiel_informatique/` |
| P1 | Matériel Informatique | Affectation d'équipements | Gestionnaire Info | En tant que gestionnaire, je veux affecter des équipements | RG-MAT-002: Un équipement par utilisateur maximum | US-MAT-002: Assigner un équipement à un utilisateur | Gestion du parc | À faire | Traçabilité des affectations | `/materiel_informatique/` | `/materiel_informatique/` |
| P1 | Matériel Bureau | Gestion du mobilier | Gestionnaire Bureau | En tant que gestionnaire bureau, je veux gérer le mobilier | RG-MAT-003: Inventaire bureau avec localisation | US-MAT-003: Gérer le mobilier de bureau | - | À faire | Gestion des espaces de travail | `/materiel_bureautique/` | `/materiel_bureautique/` |
| P1 | Matériel Bureau | Affectation mobilier | Gestionnaire Bureau | En tant que gestionnaire bureau, je veux affecter du mobilier | RG-MAT-004: Mobilier selon poste de travail | US-MAT-004: Assigner du mobilier aux employés | Gestion du mobilier | À faire | Configuration poste de travail | `/materiel_bureautique/` | `/materiel_bureautique/` |
| P1 | Commandes Informatiques | Création de commande | Gestionnaire Info | En tant que gestionnaire, je veux créer des commandes informatiques | RG-COM-001: Validation fournisseur et budget | US-COM-001: Créer une commande avec lignes | Gestion du parc | À faire | Gestion des devis et budgets | `/commande_informatique/ajouter/` | `/commande_informatique/ajouter/` |
| P1 | Commandes Informatiques | Suivi des commandes | Gestionnaire Info | En tant que gestionnaire, je veux suivre mes commandes | RG-COM-002: Statuts de commande obligatoires | US-COM-002: Voir l'état de mes commandes | Création de commande | À faire | Workflow de commande | `/commande_informatique/liste/` | `/commande_informatique/liste/` |
| P1 | Commandes Bureau | Création commande bureau | Gestionnaire Bureau | En tant que gestionnaire bureau, je veux commander du mobilier | RG-COM-003: Validation fournisseur bureau | US-COM-003: Créer commande mobilier | Gestion du mobilier | À faire | Catalogue fournisseurs bureau | `/commande_bureau/ajouter/` | `/commande_bureau/ajouter/` |
| P1 | Commandes Bureau | Suivi commandes bureau | Gestionnaire Bureau | En tant que gestionnaire bureau, je veux suivre mes commandes | RG-COM-004: Statuts spécifiques bureau | US-COM-004: Suivre commandes mobilier | Création commande bureau | À faire | Gestion des délais livraison | `/commande_bureau/liste/` | `/commande_bureau/liste/` |
| P1 | Fournisseurs | Gestion catalogue | Super Admin | En tant qu'admin, je veux gérer les fournisseurs | RG-FOU-001: Données fournisseur complètes | US-FOU-001: Ajouter/modifier fournisseurs | - | À faire | Base de données fournisseurs | `/fournisseurs/` | `/fournisseurs/` |
| P1 | Fournisseurs | Catalogue produits | Super Admin | En tant qu'admin, je veux gérer les catalogues | RG-FOU-002: Désignations et descriptions | US-FOU-002: Maintenir les catalogues produits | Gestion catalogue | À faire | Classification produits | `/fournisseurs/` | `/fournisseurs/` |
| P1 | Livraisons | Réception de livraisons | Gestionnaire Info | En tant que gestionnaire, je veux réceptionner les livraisons | RG-LIV-001: PV de réception obligatoire | US-LIV-001: Valider les livraisons reçues | Commandes | À faire | Contrôle qualité réception | `/livraison/nouvelle/` | `/livraison/nouvelle/` |
| P1 | Livraisons | Suivi des livraisons | Gestionnaire Info | En tant que gestionnaire, je veux suivre les livraisons | RG-LIV-002: Statuts de livraison | US-LIV-002: Voir l'état des livraisons | Réception de livraisons | À faire | Traçabilité complète | `/livraison/` | `/livraison/` |
| P2 | Notifications | Système de notifications | Employé | En tant qu'utilisateur, je veux recevoir des notifications | RG-NOT-001: Notifications temps réel | US-NOT-001: Voir mes notifications | Demandes Équipement | À faire | Notifications push et email | `/users/notifications-demandes/` | `/users/notifications-demandes/` |
| P2 | Notifications | Notifications garantie | Employé | En tant qu'utilisateur, je veux être alerté des garanties | RG-NOT-002: Alertes 30 jours avant expiration | US-NOT-002: Recevoir alertes garantie | Matériel Informatique | À faire | Système d'alertes automatiques | `/users/notifications-garantie/` | `/users/notifications-garantie/` |
| P2 | Dashboard | Tableau de bord employé | Employé | En tant qu'employé, je veux voir mon dashboard | RG-DASH-001: Données personnalisées par rôle | US-DASH-001: Accéder à mon tableau de bord | Authentification | À faire | Vue d'ensemble personnalisée | `/users/employe/` | `/users/employe/` |
| P2 | Dashboard | Dashboard gestionnaire info | Gestionnaire Info | En tant que gestionnaire, je veux mon dashboard | RG-DASH-002: Métriques informatiques | US-DASH-002: Voir les KPIs informatiques | Authentification | À faire | Indicateurs de performance | `/users/gestionnaire_info/` | `/users/gestionnaire_info/` |
| P2 | Dashboard | Dashboard gestionnaire bureau | Gestionnaire Bureau | En tant que gestionnaire bureau, je veux mon dashboard | RG-DASH-003: Métriques bureau | US-DASH-003: Voir les KPIs bureau | Authentification | À faire | Indicateurs bureau | `/users/gestionnaire_bureau/` | `/users/gestionnaire_bureau/` |
| P2 | Dashboard | Dashboard super admin | Super Admin | En tant qu'admin, je veux le dashboard complet | RG-DASH-004: Vue globale du système | US-DASH-004: Accéder à toutes les données | Authentification | À faire | Administration complète | `/users/superadmin/` | `/users/superadmin/` |
| P2 | Chatbot | Assistant IA | Employé | En tant qu'utilisateur, je veux poser des questions | RG-CHAT-001: Réponses basées sur la base de connaissances | US-CHAT-001: Interroger l'assistant IA | - | À faire | RAG avec base de connaissances | `/chatbot/` | `/chatbot/` |
| P2 | Chatbot | Base de connaissances | Super Admin | En tant qu'admin, je veux maintenir la base | RG-CHAT-002: Documentation à jour | US-CHAT-002: Mettre à jour la documentation | Assistant IA | À faire | Système RAG avancé | `/chatbot/` | `/chatbot/` |
| P2 | Rapports | Export Excel | Gestionnaire Info | En tant que gestionnaire, je veux exporter des données | RG-RAP-001: Formats Excel standardisés | US-RAP-001: Exporter les données en Excel | Gestion du parc | À faire | Templates Excel personnalisés | `/materiel_informatique/export_excel/` | `/materiel_informatique/export_excel/` |
| P2 | Rapports | Rapports de livraison | Gestionnaire Info | En tant que gestionnaire, je veux des rapports | RG-RAP-002: Statistiques de livraison | US-RAP-002: Générer des rapports | Livraisons | À faire | Tableaux de bord analytiques | `/livraison/rapports/` | `/livraison/rapports/` |
| P2 | Recherche | Recherche globale | Employé | En tant qu'utilisateur, je veux rechercher | RG-RECH-001: Recherche multi-critères | US-RECH-001: Trouver rapidement des informations | - | À faire | Recherche sémantique | `/users/search/` | `/users/search/` |
| P3 | Garanties | Suivi des garanties | Gestionnaire Info | En tant que gestionnaire, je veux suivre les garanties | RG-GAR-001: Alertes automatiques | US-GAR-001: Gérer les garanties | Matériel Informatique | À faire | Système d'alertes | `/users/dashboard-garantie/` | `/users/dashboard-garantie/` |
| P3 | Archives | Archivage électronique | Super Admin | En tant qu'admin, je veux archiver | RG-ARC-001: Conservation légale | US-ARC-001: Archiver les documents | Demandes Équipement | À faire | Archivage sécurisé | `/demande_equipement/archives/` | `/demande_equipement/archives/` |
| P3 | API | API REST | Super Admin | En tant qu'admin, je veux une API | RG-API-001: Documentation OpenAPI | US-API-001: Exposer les données via API | - | À faire | API RESTful complète | `/api/` | `/api/` |
| P3 | Sécurité | Audit des permissions | Super Admin | En tant qu'admin, je veux auditer | RG-SEC-001: Traçabilité des actions | US-SEC-001: Voir les logs d'audit | Authentification | À faire | Journalisation complète | `/audit/` | `/audit/` |

---

## 🎭 Personas Détaillés

### 👤 Employé
- **Rôle** : Utilisateur final du système
- **Responsabilités** : Créer des demandes, signer des décharges, consulter ses équipements
- **Accès** : Dashboard employé, demandes personnelles, notifications

### 🔧 Gestionnaire Informatique
- **Rôle** : Gestionnaire du parc informatique
- **Responsabilités** : Approuver demandes IT, gérer matériel informatique, suivre commandes IT
- **Accès** : Dashboard gestionnaire info, matériel informatique, commandes IT

### 🪑 Gestionnaire Bureau
- **Rôle** : Gestionnaire du mobilier et fournitures de bureau
- **Responsabilités** : Approuver demandes bureau, gérer mobilier, suivre commandes bureau
- **Accès** : Dashboard gestionnaire bureau, matériel bureau, commandes bureau

### 👑 Super Admin
- **Rôle** : Administrateur système
- **Responsabilités** : Gestion complète du système, utilisateurs, fournisseurs
- **Accès** : Toutes les fonctionnalités, configuration système

---

## 📋 Légende

### Priorités
- **P1** : Critique - Fonctionnalité essentielle au fonctionnement
- **P2** : Important - Fonctionnalité importante pour l'expérience utilisateur
- **P3** : Optionnel - Fonctionnalité d'amélioration ou d'optimisation

### Statuts
- **À faire** : Fonctionnalité à développer
- **En cours** : Développement en cours
- **Terminé** : Fonctionnalité livrée
- **Test** : En phase de test
- **Déployé** : En production

### Abréviations
- **US** : User Story
- **RG** : Règle de Gestion
- **EPIC** : Groupe de fonctionnalités liées
- **Feature** : Fonctionnalité spécifique
- **Persona** : Type d'utilisateur cible
