# 📊 Statuts et Transitions ParcInfo - Guide de Réalisation

## 🎯 **Statuts des Demandes d'Équipement**

### **Statuts Possibles**
```python
STATUT_CHOICES = [
    ('en_attente', 'En attente'),
    ('approuvee', 'Approuvée'),
    ('refusee', 'Refusée'),
]
```

### **Transitions de Statut**

#### **1. Création de Demande**
```
Début → en_attente (si stock disponible)
Début → refusee (si stock indisponible)
```

**Conditions :**
- `en_attente` : stock_disponible > 0
- `refusee` : stock_disponible = 0

#### **2. Traitement par Gestionnaire**
```
en_attente → approuvee (approbation)
en_attente → refusee (refus)
```

**Actions déclencheuses :**
- Gestionnaire approuve → `approuvee`
- Gestionnaire refuse → `refusee`

#### **3. Pas de Transitions Possibles**
- ❌ `approuvee` → `en_attente` (impossible)
- ❌ `approuvee` → `refusee` (impossible)
- ❌ `refusee` → `en_attente` (impossible)
- ❌ `refusee` → `approuvee` (impossible)

---

## 📦 **Statuts des Livraisons**

### **Statuts Possibles**
```python
STATUT_LIVRAISON_CHOICES = [
    ('en_attente', 'En attente'),
    ('en_cours', 'En cours'),
    ('livree', 'Livrée'),
    ('retardee', 'Retardée'),
    ('annulee', 'Annulée'),
]
```

### **Transitions de Statut**

#### **1. Création de Livraison**
```
Début → en_attente
```

#### **2. Progression de Livraison**
```
en_attente → en_cours (livraison démarrée)
en_cours → livree (livraison effectuée)
en_cours → retardee (retard détecté)
```

#### **3. Gestion des Retards**
```
retardee → en_cours (retard résolu)
retardee → livree (livraison finalisée)
```

#### **4. Annulation**
```
en_attente → annulee
en_cours → annulee
retardee → annulee
```

#### **5. Pas de Transitions Possibles**
- ❌ `livree` → `en_cours` (impossible)
- ❌ `livree` → `retardee` (impossible)
- ❌ `livree` → `annulee` (impossible)
- ❌ `annulee` → autres statuts (impossible)

---

## 🔔 **Statuts des Notifications**

### **Statuts Possibles**
```python
# Statut de lecture
lu = models.BooleanField(default=False)

# Statut de la demande concernée
STATUT_CHOICES = [
    ('en_attente', 'En attente'),
    ('approuvee', 'Approuvée'),
    ('rejetee', 'Rejetée'),
    ('refusee', 'Refusée'),
    ('en_cours', 'En cours de traitement'),
    ('terminee', 'Terminée'),
    ('en_attente_signature', 'En attente de signature'),
    ('signature_requise', 'Signature requise'),
]
```

### **Transitions de Statut**

#### **1. Création de Notification**
```
Événement → Notification créée (lu=False)
```

**Événements déclencheurs :**
- Changement de statut d'une demande
- Nouvelle demande créée
- Livraison en retard
- PV réception validé

#### **2. Lecture de Notification**
```
lu=False → lu=True
```

**Actions :**
- Utilisateur consulte la notification
- Marquage automatique comme lue
- Enregistrement de la date de lecture

---

## 🏷️ **Types de Demande**

### **Types Possibles**
```python
TYPE_DEMANDE_CHOICES = [
    ('nouveau', 'Nouveau'),
    ('renouvellement', 'Renouvellement'),
    ('reparation', 'Réparation'),
    ('service', 'Service'),
    ('deplacement', 'Déplacement'),
]
```

### **Règles de Validation**

#### **Pour les Fournitures**
```python
# Fournitures : type_demande doit être 'nouveau'
if self.type_article == 'fourniture' and self.type_demande != 'nouveau':
    raise ValidationError("Pour les fournitures, le type de demande doit être 'Nouveau'")
```

#### **Pour les Matériels**
```python
# Matériels : tous les types autorisés
# Pas de restriction spécifique
```

---

## 📋 **Catégories d'Équipement**

### **Catégories Possibles**
```python
CATEGORIE_CHOICES = [
    ('informatique', 'Informatique'),
    ('bureau', 'Bureau'),
]
```

### **Règles de Gestion**

#### **Gestionnaire Informatique**
- Accès uniquement aux demandes `categorie='informatique'`
- Peut approuver/refuser les demandes informatiques
- Peut sélectionner le matériel informatique

#### **Gestionnaire Bureau**
- Accès uniquement aux demandes `categorie='bureau'`
- Peut approuver/refuser les demandes bureau
- Peut sélectionner le matériel bureau

#### **Super Admin**
- Accès à toutes les catégories
- Peut gérer toutes les demandes
- Peut créer des commandes pour toutes les catégories

---

## 🛒 **Types d'Article**

### **Types Possibles**
```python
TYPE_ARTICLE_CHOICES = [
    ('materiel', 'Matériel'),
    ('fourniture', 'Fourniture'),
]
```

### **Règles de Validation**

#### **Pour les Matériels**
```python
# Matériels : désignation et description obligatoires
if self.type_article == 'materiel':
    if not self.designation or not self.description:
        raise ValidationError("Pour les matériels, la désignation et la description sont obligatoires")
    if self.fourniture:
        raise ValidationError("Les matériels ne doivent pas avoir de fourniture sélectionnée")
```

#### **Pour les Fournitures**
```python
# Fournitures : fourniture obligatoire, pas de désignation/description
if self.type_article == 'fourniture':
    if not self.fourniture:
        raise ValidationError("Pour les fournitures, la sélection d'une fourniture est obligatoire")
    if self.designation_info or self.description_info or self.designation_bureau or self.description_bureau:
        raise ValidationError("Les fournitures ne doivent pas avoir de désignation ou description")
```

---

## 🔧 **Statuts du Matériel**

### **Matériel Informatique**
```python
STATUT_CHOICES = [
    ('nouveau', 'Nouveau'),
    ('affecte', 'Affecté'),
    ('en panne', 'En panne'),
    ('en maintenance', 'En maintenance'),
]
```

### **Matériel Bureau**
```python
# Statut par défaut : 'Opérationnel'
# Pas de statuts spécifiques définis dans le modèle
```

### **Transitions de Statut Matériel**

#### **1. Matériel Informatique**
```
nouveau → affecte (affectation à un utilisateur)
affecte → en panne (déclaration de panne)
en panne → en maintenance (mise en maintenance)
en maintenance → affecte (maintenance terminée)
```

#### **2. Règles d'Affectation**
```python
# Seuls les matériels avec statut='nouveau' et utilisateur=None peuvent être affectés
materiels_disponibles = MaterielInformatique.objects.filter(
    ligne_commande__designation=demande.designation_info,
    ligne_commande__description=demande.description_info,
    utilisateur__isnull=True,
    statut='nouveau'
)
```

---

## 📊 **Modes de Passation des Commandes**

### **Modes Possibles**
```python
MODE_PASSATION_CHOICES = [
    ('BC', 'Bon de Commande'),
    ('Contrat', 'Contrat'),
    ('AO', "Appel d'Offres"),
]
```

### **Utilisation**
- **BC** : Commandes simples et directes
- **Contrat** : Commandes avec engagement contractuel
- **AO** : Commandes nécessitant une procédure d'appel d'offres

---

## 🎯 **Points de Décision dans les Workflows**

### **1. Vérification Stock**
```
Question : "Stock disponible ?"
Acteur : Système
Décision : Automatique
Résultats :
  - Oui → Statut 'en_attente'
  - Non → Statut 'refusee'
```

### **2. Validation Demande**
```
Question : "Demande valide ?"
Acteur : Gestionnaire
Décision : Manuelle
Résultats :
  - Oui → Statut 'approuvee'
  - Non → Statut 'refusee'
```

### **3. Disponibilité Matériel**
```
Question : "Matériel disponible ?"
Acteur : Gestionnaire
Décision : Manuelle
Résultats :
  - Oui → Sélection matériel
  - Non → Retour à l'analyse
```

### **4. Validation Commande**
```
Question : "Commande > seuil ?"
Acteur : Super Admin
Décision : Manuelle
Résultats :
  - Oui → Validation requise
  - Non → Validation automatique
```

### **5. Conformité Fournisseur**
```
Question : "Fournisseur approuvé ?"
Acteur : Super Admin
Décision : Manuelle
Résultats :
  - Oui → Commande validée
  - Non → Commande rejetée
```

### **6. Notification Requise**
```
Question : "Notification requise ?"
Acteur : Système
Décision : Automatique
Résultats :
  - Oui → Notification générée
  - Non → Pas de notification
```

---

## 🔄 **Flux de Retour et Exceptions**

### **1. Demande Refusée**
```
Flux : Demande refusée → Retour à la création
Raison : Stock indisponible ou validation négative
Action : Employé peut créer une nouvelle demande
```

### **2. Matériel Non Disponible**
```
Flux : Matériel non disponible → Retour à l'analyse
Raison : Matériel spécifique non trouvé
Action : Gestionnaire peut sélectionner un autre matériel
```

### **3. PV Non Reçu**
```
Flux : PV non reçu → Retour à la validation
Raison : Document manquant ou incomplet
Action : Gestionnaire doit valider le PV
```

### **4. Livraison en Retard**
```
Flux : Livraison en retard → Notification automatique
Raison : Date de livraison dépassée
Action : Système génère une alerte
```

---

## 📋 **Checklist pour votre Diagramme**

### **Statuts à Inclure**
- [ ] Statuts des demandes (en_attente, approuvee, refusee)
- [ ] Statuts des livraisons (en_attente, en_cours, livree, retardee, annulee)
- [ ] Statuts des notifications (lu/non lu)
- [ ] Statuts du matériel (nouveau, affecte, en panne, en maintenance)

### **Transitions à Représenter**
- [ ] Toutes les transitions de statut possibles
- [ ] Flux de retour en cas d'erreur
- [ ] Notifications automatiques
- [ ] Validations manuelles

### **Points de Décision**
- [ ] Vérification stock automatique
- [ ] Validation demande par gestionnaire
- [ ] Sélection matériel
- [ ] Validation commande par Super Admin
- [ ] Conformité fournisseur
- [ ] Génération notifications

### **Acteurs et Permissions**
- [ ] Employé (création, consultation, signature)
- [ ] Gestionnaire Informatique (demandes info uniquement)
- [ ] Gestionnaire Bureau (demandes bureau uniquement)
- [ ] Super Admin (toutes les permissions)
- [ ] Système (automatisations)

---

**Date de création** : 2025-01-15  
**Version** : 1.0  
**Auteur** : Équipe ParcInfo  
**Statut** : Guide complet pour réalisation ✅
