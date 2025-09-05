# Interfaces des Demandes d'Équipement - ParcInfo

## Interface de Nouvelle Demande d'Équipement

### Vue d'ensemble
L'interface de nouvelle demande d'équipement constitue le point d'entrée principal pour les utilisateurs souhaitant soumettre une demande de matériel informatique ou bureautique. Cette interface moderne et intuitive, développée avec Django et Tailwind CSS, offre une expérience utilisateur fluide et responsive.

### Design et Architecture
L'interface présente un design épuré avec un dégradé de fond bleu-indigo qui crée une ambiance professionnelle et moderne. Le formulaire est encapsulé dans une carte avec effet de flou (backdrop-filter) et transparence, donnant un aspect premium à l'interface. L'utilisation de la police Inter garantit une excellente lisibilité sur tous les appareils.

### Structure du Formulaire
Le formulaire est organisé en sections logiques permettant une saisie progressive et structurée des informations :

**Section Catégorie et Type :**
- **Catégorie** : Choix entre "Informatique" et "Bureau" avec des badges colorés distinctifs
- **Type d'article** : Sélection entre "Matériel" et "Consommable"
- **Type de demande** : Options "Nouvelle acquisition", "Remplacement" ou "Maintenance"

**Section Désignation et Description :**
- **Désignation** : Menu déroulant dynamique qui se met à jour selon la catégorie sélectionnée
- **Description** : Sous-catégorisation qui s'adapte à la désignation choisie
- **Quantité** : Champ numérique avec validation

**Section Justification :**
- **Justification** : Zone de texte libre pour expliquer le besoin
- **Urgence** : Indicateur d'urgence avec options "Normale", "Urgente" ou "Critique"

### Fonctionnalités Interactives
L'interface intègre plusieurs fonctionnalités JavaScript avancées :

**Champs Conditionnels :**
- Les champs de désignation et description s'affichent dynamiquement selon le type d'article sélectionné
- Les options de catégorie filtrent automatiquement les désignations disponibles
- Animation fluide des transitions avec des effets de fade et de slide

**Validation en Temps Réel :**
- Vérification instantanée de la disponibilité du stock
- Messages d'erreur contextuels et informatifs
- Indicateurs visuels de statut (succès, erreur, avertissement)

**API Dynamique :**
- Appels AJAX pour récupérer les désignations selon la catégorie
- Filtrage des descriptions selon les permissions utilisateur
- Mise à jour asynchrone des options sans rechargement de page

### Gestion des Permissions
L'interface adapte son contenu selon le profil utilisateur :
- **Employés** : Accès limité aux descriptions publiques uniquement
- **Gestionnaires** : Accès complet à toutes les désignations et descriptions
- **Super Admin** : Accès illimité à toutes les fonctionnalités

### Responsive Design
L'interface s'adapte parfaitement à tous les écrans :
- **Desktop** : Layout en grille multi-colonnes optimisé
- **Tablet** : Adaptation automatique des colonnes
- **Mobile** : Stack vertical avec boutons tactiles optimisés

---

## Interface de Traitement des Demandes

### Vue d'ensemble
L'interface de traitement des demandes est réservée aux gestionnaires et administrateurs. Elle permet de consulter, approuver, refuser et gérer le cycle de vie complet des demandes d'équipement soumises par les utilisateurs.

### Tableau de Bord Principal
L'interface principale présente un tableau complet avec les informations essentielles de chaque demande :

**Colonnes d'Information :**
- **Date de demande** : Format français (dd/mm/yyyy)
- **Demandeur** : Nom complet avec avatar généré automatiquement
- **Catégorie** : Badge coloré (bleu pour informatique, vert pour bureau)
- **Type d'article** : Matériel ou Consommable
- **Désignation et Description** : Détails techniques de l'équipement
- **Code inventaire** : Identifiant unique du matériel
- **Effectif total** : Nombre total d'unités commandées
- **Stock disponible** : Quantité en stock non affectée
- **Date d'affectation** : Quand le matériel a été attribué
- **Statut** : Badge coloré selon l'état (en attente, approuvée, refusée, etc.)
- **Décharge** : Indicateur de signature électronique

### Fonctionnalités de Gestion

**Filtrage et Recherche :**
- Filtrage par catégorie (informatique/bureau)
- Recherche par nom de demandeur
- Tri par date, statut ou urgence
- Pagination automatique pour les grandes listes

**Actions Disponibles :**
- **Approuver** : Valider la demande et générer une décharge
- **Refuser** : Rejeter la demande avec justification
- **Marquer en cours** : Indiquer le début du traitement
- **Terminer** : Finaliser le processus
- **Affecter matériel** : Assigner un équipement spécifique
- **Consulter détails** : Voir tous les détails de la demande

### Interface de Traitement Détaillé
L'interface d'approbation offre une vue complète de chaque demande :

**Informations du Demandeur :**
- Nom complet et email
- Service et fonction
- Historique des demandes précédentes

**Détails Techniques :**
- Spécifications complètes du matériel
- Justification détaillée
- Niveau d'urgence
- Date de soumission

**Gestion du Stock :**
- Affichage du stock disponible en temps réel
- Sélection manuelle du matériel à affecter
- Vérification automatique de disponibilité
- Code inventaire généré automatiquement

**Actions de Traitement :**
- Boutons d'action contextuels selon le statut
- Confirmation avant actions critiques
- Messages de feedback en temps réel
- Génération automatique de PDF de décharge

### Gestion des Décharges
L'interface intègre un système complet de gestion des décharges :

**Génération Automatique :**
- Création de PDF de décharge lors de l'approbation
- Inclusion automatique des informations de la demande
- Signature électronique sécurisée
- Stockage sécurisé des documents

**Interface de Signature :**
- Canvas de signature tactile
- Validation de la signature électronique
- Horodatage automatique
- Sauvegarde sécurisée des signatures

### Tableau de Bord Analytique
L'interface inclut des métriques importantes :

**Statistiques en Temps Réel :**
- Nombre de demandes en attente
- Demandes approuvées aujourd'hui
- Taux d'approbation global
- Temps moyen de traitement

**Indicateurs Visuels :**
- Graphiques de progression
- Badges de statut colorés
- Indicateurs d'urgence
- Alertes de stock faible

### Sécurité et Permissions
L'interface respecte strictement la hiérarchie des permissions :

**Gestionnaires Informatique :**
- Accès uniquement aux demandes informatiques
- Actions limitées à leur domaine de compétence

**Gestionnaires Bureau :**
- Accès uniquement aux demandes bureautiques
- Gestion complète de leur catégorie

**Super Administrateurs :**
- Accès à toutes les demandes
- Actions illimitées
- Gestion des utilisateurs et permissions

### Notifications et Alertes
Le système intègre un système de notifications complet :

**Notifications en Temps Réel :**
- Alertes de nouvelles demandes
- Rappels de demandes en attente
- Notifications de stock faible
- Confirmations d'actions

**Messages Contextuels :**
- Feedback immédiat après chaque action
- Messages d'erreur détaillés
- Confirmations de succès
- Avertissements de sécurité

### Export et Reporting
L'interface permet l'export des données :

**Formats Supportés :**
- Export PDF des demandes
- Export Excel des listes
- Génération de rapports mensuels
- Archives automatiques

**Fonctionnalités d'Archivage :**
- Conservation des demandes traitées
- Recherche dans les archives
- Restauration si nécessaire
- Sauvegarde automatique

Cette interface de traitement constitue le cœur du système de gestion des demandes d'équipement, offrant aux gestionnaires tous les outils nécessaires pour une gestion efficace et transparente du parc informatique et bureautique.

---

## Interface "Mes Demandes"

L'interface "Mes Demandes" constitue le tableau de bord personnel de chaque utilisateur, présentant une vue d'ensemble organisée de toutes ses demandes d'équipement. Cette interface intuitive affiche en priorité les décharges à signer dans une section distincte avec un encadré jaune, suivie de toutes les autres demandes organisées chronologiquement. Chaque demande présente les informations essentielles (date, catégorie, type, désignation, statut) avec des badges colorés pour une identification rapide. L'interface propose des actions contextuelles adaptées au statut de chaque demande : modification et suppression pour les demandes en attente, signature de décharge pour les demandes approuvées, et consultation des documents pour les demandes finalisées. Le design responsive s'adapte parfaitement à tous les appareils, offrant une navigation fluide et des boutons tactiles optimisés sur mobile. Cette interface centralisée permet à chaque utilisateur de suivre efficacement l'évolution de ses demandes et d'effectuer les actions nécessaires pour finaliser le processus d'obtention d'équipement.

---

## Interface "Mes Équipements Informatiques"

L'interface "Mes Équipements Informatiques" offre un inventaire complet de tous les équipements informatiques affectés à l'utilisateur connecté. Cette interface présente une structure similaire à celle des équipements bureautiques mais avec une identité visuelle distincte utilisant des couleurs bleues et des icônes d'ordinateur. Pour les employés, elle affiche un design moderne avec un en-tête dégradé bleu-violet et un tableau détaillé présentant la désignation, description et statut de chaque équipement avec des badges bleus caractéristiques. Pour les autres utilisateurs, elle propose une vue simplifiée avec les informations essentielles. L'interface inclut un compteur dynamique du nombre d'équipements et des actions contextuelles comme "Voir détails" pour chaque équipement. En cas d'absence d'équipements, l'interface affiche un état vide avec une icône d'ordinateur, un message d'encouragement et un bouton direct vers le formulaire de demande d'équipement. Le design responsive avec des effets de survol bleus et des transitions fluides garantit une expérience utilisateur cohérente et professionnelle.

---

## Interface "Mes Équipements Bureautiques"

L'interface "Mes Équipements Bureautiques" présente un inventaire personnel de tous les équipements bureautiques affectés à l'utilisateur connecté. Cette interface adaptative s'affiche différemment selon le profil utilisateur : pour les employés, elle offre un design moderne avec un en-tête coloré et un tableau détaillé présentant la désignation, description et statut de chaque équipement avec des badges violets distinctifs. Pour les autres utilisateurs, elle propose une vue simplifiée avec les informations essentielles. L'interface inclut un compteur dynamique du nombre d'équipements et propose des actions contextuelles comme "Voir détails" pour chaque équipement. En cas d'absence d'équipements, l'interface affiche un état vide avec un message d'encouragement et un bouton direct vers le formulaire de demande d'équipement. Le design responsive avec des effets de survol et des transitions fluides garantit une expérience utilisateur optimale sur tous les appareils.

---

## Interface Chatbot Assistant IA

L'interface Chatbot Assistant IA constitue un assistant intelligent intégré au système ParcInfo, offrant une interaction conversationnelle naturelle pour la gestion du parc informatique et bureautique. Cette interface moderne présente un design épuré avec un en-tête dégradé indigo-violet et une zone de chat responsive. L'assistant propose des suggestions rapides pour les questions fréquentes et affiche les messages dans des bulles distinctes avec des avatars différenciés (robot pour l'assistant, utilisateur pour l'humain). L'interface intègre des fonctionnalités avancées comme la saisie en temps réel, des indicateurs de frappe, et un système de suggestions contextuelles. Le chatbot peut répondre aux questions sur le matériel, les commandes, les fournisseurs, les livraisons, les demandes d'équipement et les garanties, en utilisant les données de la base SQL. L'interface inclut également un modal d'aide avec des exemples de questions et des conseils d'utilisation, ainsi que des fonctionnalités de copie de messages et de feedback utilisateur. Le design responsive et les animations fluides garantissent une expérience utilisateur intuitive et professionnelle.

---

## Interface Dashboard Garantie

L'interface Dashboard Garantie constitue un tableau de bord analytique avancé développé avec Streamlit pour le suivi et la gestion des garanties du parc informatique et bureautique. Cette interface présente un design ultra-moderne avec un en-tête dégradé professionnel et une mise en page responsive adaptée aux différents rôles utilisateur. Le dashboard affiche des métriques clés en temps réel : nombre total de commandes, garanties expirées, critiques (≤15 jours) et urgentes (≤30 jours) avec des indicateurs visuels colorés. L'interface intègre une chronologie interactive des garanties sous forme de graphique Gantt, permettant de visualiser les dates de fin de garantie par commande avec un code couleur selon l'urgence. Des analyses détaillées par fournisseur sont proposées avec des graphiques en barres et des statistiques comparatives. L'interface inclut des filtres avancés par statut, type d'équipement et fournisseur, ainsi qu'un tableau interactif avec tri et pagination. Le dashboard s'adapte automatiquement aux permissions utilisateur : vue complète pour les super administrateurs, filtrage par catégorie pour les gestionnaires, et accès en lecture seule pour les employés. Le design professionnel avec des animations fluides et une navigation intuitive garantit une expérience utilisateur optimale pour la surveillance des garanties.