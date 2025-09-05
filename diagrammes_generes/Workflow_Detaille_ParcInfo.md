# 🔄 Workflow Détaillé ParcInfo - Réalisation Manuelle

## 📋 Vue d'Ensemble des Processus

Basé sur l'analyse approfondie du code source ParcInfo, voici tous les workflows détaillés que vous pouvez réaliser vous-même.

## 🎯 **Workflow 1 : Demande d'Équipement**

### **Acteurs Impliqués**
- **Employé** : Utilisateur final
- **Système** : Logique automatisée
- **Gestionnaire Informatique** : Pour demandes informatiques
- **Gestionnaire Bureau** : Pour demandes bureautiques

### **Étapes Détaillées**

#### **1. Création de la Demande (Employé)**
```
Début → Employé remplit formulaire → Système traite
```

**Actions Employé :**
- Sélectionne catégorie (informatique/bureau)
- Choisit type d'article (matériel/fourniture)
- Spécifie type de demande (nouveau/renouvellement/réparation/service/déplacement)
- Remplit désignation et description
- Soumet la demande

**Actions Système :**
- Vérifie automatiquement la disponibilité du stock
- Définit le statut selon la disponibilité :
  - `refusee` si stock = 0
  - `en_attente` si stock > 0
- Crée la demande en base de données

#### **2. Vérification Stock (Système)**
```
Système vérifie stock → Décision automatique
```

**Logique de vérification :**
```python
if demande.type_article == 'materiel':
    if demande.categorie == 'informatique':
        stock_disponible = MaterielInformatique.objects.filter(
            ligne_commande__designation=demande.designation_info,
            ligne_commande__description=demande.description_info,
            utilisateur__isnull=True,
            statut='nouveau'
        ).count()
    elif demande.categorie == 'bureau':
        stock_disponible = MaterielBureau.objects.filter(
            ligne_commande__designation=demande.designation_bureau,
            ligne_commande__description=demande.description_bureau,
            utilisateur__isnull=True
        ).count()
    
    rupture = stock_disponible == 0
    demande.statut = 'refusee' if rupture else 'en_attente'
```

#### **3. Notification Gestionnaire (Système)**
```
Système → Notification automatique → Gestionnaire approprié
```

**Système de notifications :**
- Notification envoyée automatiquement au gestionnaire approprié
- Gestionnaire Informatique pour demandes informatiques
- Gestionnaire Bureau pour demandes bureautiques

#### **4. Analyse et Approbation (Gestionnaire)**
```
Gestionnaire reçoit notification → Analyse → Décision
```

**Actions Gestionnaire :**
- Consulte la demande
- Vérifie les détails (désignation, description, type)
- Prend décision : Approuver ou Refuser
- Si approuvé : Sélectionne le matériel spécifique

**Statuts possibles :**
- `approuvee` : Demande validée
- `refusee` : Demande rejetée

#### **5. Signature Décharge (Employé)**
```
Employé → Signature digitale → Validation
```

**Actions Employé :**
- Consulte la demande approuvée
- Signe la décharge digitale
- Confirme la réception

#### **6. Affectation Matériel (Système)**
```
Système → Affectation automatique → Archivage
```

**Actions Système :**
- Affecte le matériel sélectionné à l'employé
- Met à jour le statut du matériel
- Crée l'archive de la décharge

---

## 🛒 **Workflow 2 : Gestion des Commandes**

### **Acteurs Impliqués**
- **Super Admin** : Création et gestion
- **Fournisseur** : Livraison
- **Système** : Suivi et notifications

### **Étapes Détaillées**

#### **1. Création Commande (Super Admin)**
```
Super Admin → Création commande → Lignes de commande
```

**Actions Super Admin :**
- Choisit le type de commande (informatique/bureau)
- Sélectionne le fournisseur
- Définit le mode de passation (BC/Contrat/AO)
- Crée les lignes de commande avec :
  - Désignation
  - Description
  - Quantité
  - Prix unitaire
- Définit la durée de garantie

#### **2. Validation Commande (Système)**
```
Système → Validation → Enregistrement
```

**Actions Système :**
- Calcule le montant total
- Génère le numéro de commande
- Enregistre la commande en base

#### **3. Transmission Fournisseur (Super Admin)**
```
Super Admin → Transmission → Fournisseur
```

**Actions Super Admin :**
- Transmet la commande au fournisseur
- Définit la date de réception prévue

#### **4. Suivi Livraison (Système)**
```
Système → Suivi → Notifications
```

**Actions Système :**
- Suit les dates de livraison
- Génère des alertes en cas de retard
- Met à jour les statuts

---

## 📦 **Workflow 3 : Gestion des Livraisons**

### **Acteurs Impliqués**
- **Gestionnaire** : Validation et réception
- **Système** : Suivi et notifications
- **Super Admin** : Supervision

### **Étapes Détaillées**

#### **1. Création Livraison (Gestionnaire)**
```
Gestionnaire → Création livraison → Suivi
```

**Actions Gestionnaire :**
- Crée une nouvelle livraison
- Associe la commande correspondante
- Définit la date de livraison prévue
- Spécifie les notes

#### **2. Suivi Statut (Système)**
```
Système → Suivi automatique → Mise à jour statuts
```

**Statuts de livraison :**
- `en_attente` : Livraison créée
- `en_cours` : Livraison en cours
- `livree` : Livraison effectuée
- `retardee` : Livraison en retard
- `annulee` : Livraison annulée

#### **3. Réception et Contrôle (Gestionnaire)**
```
Gestionnaire → Contrôle → Validation
```

**Actions Gestionnaire :**
- Vérifie la conformité de la livraison
- Contrôle la qualité du matériel
- Valide la réception

#### **4. Validation PV Réception (Gestionnaire)**
```
Gestionnaire → Validation PV → Archivage
```

**Actions Gestionnaire :**
- Valide le procès-verbal de réception
- Confirme la conformité
- Marque le PV comme reçu

#### **5. Archivage (Système)**
```
Système → Archivage → Traçabilité
```

**Actions Système :**
- Archive les documents de réception
- Met à jour l'historique
- Génère les rapports

---

## 🔔 **Workflow 4 : Système de Notifications**

### **Acteurs Impliqués**
- **Système** : Génération automatique
- **Utilisateurs** : Réception et lecture

### **Étapes Détaillées**

#### **1. Déclenchement Notification (Système)**
```
Changement statut → Système détecte → Notification générée
```

**Événements déclencheurs :**
- Changement de statut d'une demande
- Nouvelle demande créée
- Livraison en retard
- PV réception validé

#### **2. Génération Notification (Système)**
```
Système → Création notification → Envoi
```

**Types de notifications :**
- `demande_equipement` : Pour les demandes d'équipement
- `demande_bureau` : Pour les demandes bureautiques

**Contenu notification :**
- Titre avec ID demande et statut
- Message détaillé
- Statut de la demande
- ID de la demande concernée

#### **3. Réception et Lecture (Utilisateur)**
```
Utilisateur → Réception → Lecture → Marquage lu
```

**Actions Utilisateur :**
- Consulte les notifications
- Lit le contenu
- Marque comme lue
- Accède à la demande concernée

---

## 👥 **Workflow 5 : Gestion des Rôles et Permissions**

### **Acteurs Impliqués**
- **Employé** : Utilisateur de base
- **Gestionnaire Informatique** : Gestion informatique
- **Gestionnaire Bureau** : Gestion bureautique
- **Super Admin** : Administration complète

### **Permissions Détaillées**

#### **Employé**
- Créer des demandes d'équipement
- Consulter ses demandes
- Signer des décharges
- Consulter ses notifications

#### **Gestionnaire Informatique**
- Recevoir notifications demandes informatiques
- Approuver/refuser demandes informatiques
- Sélectionner matériel informatique
- Créer livraisons informatiques
- Valider PV réception informatiques

#### **Gestionnaire Bureau**
- Recevoir notifications demandes bureau
- Approuver/refuser demandes bureau
- Sélectionner matériel bureau
- Créer livraisons bureau
- Valider PV réception bureau

#### **Super Admin**
- Toutes les permissions
- Créer des commandes
- Gérer les fournisseurs
- Valider tous les PV
- Accès à tous les rapports

---

## 📊 **Workflow 6 : Archivage et Traçabilité**

### **Acteurs Impliqués**
- **Système** : Archivage automatique
- **Utilisateurs** : Consultation

### **Étapes Détaillées**

#### **1. Archivage Décharge (Système)**
```
Signature décharge → Système → Archivage automatique
```

**Actions Système :**
- Génère le PDF de décharge
- Crée l'archive électronique
- Attribue un numéro d'archive unique
- Enregistre les métadonnées

#### **2. Archivage Livraison (Système)**
```
Validation PV → Système → Archivage
```

**Actions Système :**
- Archive le PV de réception
- Enregistre la traçabilité
- Met à jour l'historique

#### **3. Consultation Archives (Utilisateurs)**
```
Utilisateur → Consultation → Recherche
```

**Actions Utilisateur :**
- Consulte les archives
- Recherche par critères
- Télécharge les documents

---

## 🎨 **Éléments Visuels pour votre Diagramme**

### **Symboles à Utiliser**
- **Rectangle arrondi** : Activités/Processus
- **Losange** : Points de décision
- **Cercle plein** : Début/Fin
- **Flèche pleine** : Flux principal
- **Flèche pointillée rouge** : Retour/Erreur
- **Flèche bleue** : Notifications

### **Couleurs par Swimlane**
- **Employé** : Bleu clair (#E3F2FD)
- **Gestionnaire Informatique** : Violet clair (#F3E5F5)
- **Gestionnaire Bureau** : Orange clair (#FFF3E0)
- **Super Admin** : Vert clair (#E8F5E8)
- **Système** : Rose clair (#FCE4EC)

### **Points de Décision Clés**
1. **Stock disponible ?** (Système)
2. **Demande valide ?** (Gestionnaire)
3. **Matériel disponible ?** (Gestionnaire)
4. **Commande > seuil ?** (Super Admin)
5. **Fournisseur approuvé ?** (Super Admin)
6. **Notification requise ?** (Système)

### **Flux de Retour**
- Demande non conforme → Retour création
- Stock insuffisant → Retour consultation
- PV non reçu → Retour validation

---

## 📋 **Checklist de Réalisation**

### **Éléments à Inclure**
- [ ] 5 swimlanes distinctes
- [ ] Points de début et fin
- [ ] Tous les points de décision
- [ ] Flux de notifications
- [ ] Flux de retour
- [ ] Légende complète
- [ ] Informations techniques

### **Validation**
- [ ] Vérifier la cohérence avec le code
- [ ] Tester les flux de retour
- [ ] Valider les permissions
- [ ] Confirmer les statuts

---

**Date de création** : 2025-01-15  
**Version** : 1.0  
**Auteur** : Équipe ParcInfo  
**Statut** : Prêt pour réalisation ✅
