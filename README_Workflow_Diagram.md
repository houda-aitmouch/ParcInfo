# 🎨 Générateur de Diagrammes de Workflow ParcInfo

Ce module génère automatiquement des diagrammes de workflow visuels pour le système ParcInfo, basés sur le workflow manuel documenté.

## 📋 Fonctionnalités

- **Workflow Complet** : Diagramme détaillé du processus de gestion d'équipement
- **Rôles et Responsabilités** : Visualisation de la hiérarchie des acteurs
- **Couleurs par Rôle** : Code couleur pour identifier facilement les responsabilités
- **Format Professionnel** : Diagrammes prêts pour présentation et documentation

## 🚀 Installation et Utilisation

### Prérequis

1. **Python 3.7+** installé
2. **Graphviz système** installé (voir instructions ci-dessous)
3. **pip** pour installer les dépendances Python

### Installation de Graphviz

#### macOS
```bash
brew install graphviz
```

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install graphviz
```

#### CentOS/RHEL
```bash
sudo yum install graphviz
```

#### Windows
1. Télécharger depuis https://graphviz.org/
2. Installer et ajouter au PATH système

### Installation des Dépendances Python

```bash
pip3 install -r requirements_graphviz.txt
```

## 🎯 Utilisation

### Méthode 1 : Script Automatique (Recommandé)

```bash
./launch_workflow_diagram.sh
```

### Méthode 2 : Exécution Directe

```bash
python3 generate_workflow_diagram.py
```

### Méthode 3 : Depuis le Répertoire Parent

```bash
cd ParcInfo
python3 generate_workflow_diagram.py
```

## 📊 Fichiers Générés

Le script génère deux diagrammes dans le dossier `diagrammes_generes/` :

### 1. `workflow_parcinfo_complet.png`
**Workflow principal complet** incluant :
- 19 étapes détaillées du processus
- Points de décision (stock, approbation, conformité)
- Code couleur par rôle d'acteur
- Flux principal et flux de commandes

### 2. `roles_parcinfo.png`
**Diagramme des rôles et responsabilités** montrant :
- Hiérarchie des acteurs
- Responsabilités principales de chaque rôle
- Relations entre les acteurs

## 🎨 Code Couleur

| Rôle | Couleur | Responsabilités |
|------|---------|-----------------|
| **Employé** | 🔵 Bleu clair | Création demandes, signature décharges |
| **Secrétaire** | 🟣 Violet clair | Enregistrement, notifications, archivage |
| **Gestionnaire Info** | 🟢 Vert clair | Traitement demandes info, gestion stock |
| **Gestionnaire Bureau** | 🟠 Orange clair | Traitement demandes bureau, gestion stock |
| **Super Admin** | 🟢 Vert très clair | Validation commandes, supervision |
| **Système** | 🔴 Rouge très clair | Notifications automatiques |

## 📋 Workflow Généré

Le diagramme principal couvre les 5 workflows documentés :

### 1. **Demande d'Équipement**
- Création de demande (Employé)
- Enregistrement et classement (Secrétaire)
- Vérification stock (Gestionnaire)
- Analyse et décision (Gestionnaire)

### 2. **Affectation Matériel**
- Préparation matériel (Gestionnaire)
- Affectation et mise à jour registre (Gestionnaire)
- Remise matériel (Employé)

### 3. **Gestion Commandes**
- Identification besoin (Gestionnaire)
- Validation et création (Super Admin)
- Transmission fournisseur (Super Admin)
- Suivi commande (Secrétaire)

### 4. **Réception et Contrôle**
- Réception physique (Gestionnaire)
- Contrôle qualité (Gestionnaire)
- Validation conformité (Super Admin)
- Mise en stock (Gestionnaire)

### 5. **Notifications et Archivage**
- Notification acteurs (Secrétaire)
- Archivage documents (Secrétaire)

## 🔧 Personnalisation

### Modifier les Couleurs

Éditez le dictionnaire `roles_colors` dans `generate_workflow_diagram.py` :

```python
roles_colors = {
    'Employé': '#E3F2FD',           # Bleu clair
    'Secrétaire': '#F3E5F5',        # Violet clair
    # ... autres couleurs
}
```

### Modifier la Taille

Changez les paramètres `size` dans les fonctions :

```python
dot.attr(rankdir='TB', size='16,12', dpi='300')
```

### Ajouter de Nouveaux Nœuds

Ajoutez de nouveaux nœuds dans la fonction `create_workflow_diagram()` :

```python
dot.node('NouveauNoeud', 'Description du nœud', 
         **node_styles['process'], fillcolor=roles_colors['Employé'])
```

## 🐛 Dépannage

### Erreur "Graphviz not found"
```bash
# Vérifier l'installation
dot -V

# Réinstaller si nécessaire
brew install graphviz  # macOS
sudo apt-get install graphviz  # Ubuntu
```

### Erreur "Module graphviz not found"
```bash
pip3 install graphviz
```

### Diagramme trop petit/grand
Modifiez le paramètre `size` dans le script :
```python
dot.attr(size='20,15')  # Plus grand
dot.attr(size='12,8')   # Plus petit
```

## 📈 Utilisation Avancée

### Générer en SVG
Modifiez le format dans le script :
```python
dot = Digraph('Workflow_ParcInfo', format='svg')
```

### Générer en PDF
```python
dot = Digraph('Workflow_ParcInfo', format='pdf')
```

### Personnaliser les Styles
```python
node_styles = {
    'process': {'shape': 'box', 'style': 'filled,rounded', 'penwidth': '2'},
    'decision': {'shape': 'diamond', 'style': 'filled', 'penwidth': '2'},
    # ...
}
```

## 📞 Support

Pour toute question ou problème :
1. Vérifiez les prérequis d'installation
2. Consultez la section dépannage
3. Vérifiez que Graphviz système est correctement installé

---

**Auteur** : Équipe ParcInfo  
**Date** : 2025-01-15  
**Version** : 1.0  
**Statut** : ✅ Prêt à l'utilisation
