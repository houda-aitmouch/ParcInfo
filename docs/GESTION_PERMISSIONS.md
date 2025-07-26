# 📋 Gestion des Permissions et Groupes - ParcInfo

## 🎯 Vue d'ensemble

Ce document décrit la gestion des permissions et groupes d'utilisateurs dans l'application ParcInfo, avec une interface Django Admin personnalisée pour une meilleure expérience utilisateur.

## 👥 Groupes d'utilisateurs

### 1. **Super Admin** 🔴
- **Accès complet** à toutes les fonctionnalités
- **166 permissions** au total
- **Gestion** de tous les utilisateurs et groupes
- **Configuration** système complète

### 2. **Gestionnaire Informatique** 🔵
- **19 permissions** spécifiques
- **Gestion** des commandes informatiques (CRUD complet)
- **Gestion** des matériels informatiques (CRUD complet)
- **Export** des données informatiques
- **Lecture seule** des fournisseurs

**Permissions principales :**
- `view_commande_informatique`, `add_commande_informatique`, `change_commande_informatique`, `delete_commande_informatique`
- `export_commande_informatique`, `approve_commande_informatique`
- `view_materiel_informatique`, `add_materiel_informatique`, `change_materiel_informatique`, `delete_materiel_informatique`
- `export_materiel_informatique`, `assign_materiel_informatique`, `maintenance_materiel_informatique`

### 3. **Gestionnaire Bureau** 🟢
- **19 permissions** spécifiques
- **Gestion** des commandes bureau (CRUD complet)
- **Gestion** des matériels bureautiques (CRUD complet)
- **Export** des données bureau
- **Lecture seule** des fournisseurs

**Permissions principales :**
- `view_commande_bureau`, `add_commande_bureau`, `change_commande_bureau`, `delete_commande_bureau`
- `export_commande_bureau`, `approve_commande_bureau`
- `view_materiel_bureautique`, `add_materiel_bureautique`, `change_materiel_bureautique`, `delete_materiel_bureautique`
- `export_materiel_bureautique`, `assign_materiel_bureautique`, `maintenance_materiel_bureautique`

### 4. **Employé** 🟡
- **8 permissions** en lecture seule
- **Consultation** des commandes et matériels
- **Aucune modification** autorisée

**Permissions principales :**
- `view_commande_informatique`, `view_commande_bureau`
- `view_materiel_informatique`, `view_materiel_bureautique`
- `view_fournisseur`

## 🔐 Types de Permissions

### Permissions CRUD Standard
- **View** : Consulter les données
- **Add** : Ajouter de nouveaux éléments
- **Change** : Modifier les éléments existants
- **Delete** : Supprimer des éléments

### Permissions Spécialisées
- **Export** : Exporter les données en Excel
- **Approve** : Approuver les commandes
- **Assign** : Assigner des matériels aux utilisateurs
- **Maintenance** : Gérer la maintenance des matériels

## 🎨 Interface Admin Personnalisée

### Fonctionnalités
1. **Affichage coloré** des groupes
2. **Résumé des permissions** par utilisateur
3. **Organisation par application** des permissions
4. **Compteurs** de permissions par groupe
5. **Interface responsive** et moderne

### Couleurs par Application
- 🔵 **Commandes Informatiques** : #007bff
- 🟢 **Commandes Bureau** : #28a745
- 🟡 **Matériels Informatiques** : #ffc107
- 🔴 **Matériels Bureautiques** : #dc3545
- 🟣 **Fournisseurs** : #6f42c1
- 🔵 **Utilisateurs** : #17a2b8

## 🚀 Utilisation

### 1. Accès à l'Admin
```
URL: http://127.0.0.1:8000/admin/
Utilisateur: superadmin
Mot de passe: superadmin123
```

### 2. Gestion des Groupes
1. Aller dans **Authentication and Authorization > Groups**
2. Cliquer sur un groupe pour le modifier
3. Utiliser l'interface organisée par catégories
4. Utiliser les boutons "Sélectionner tout" par catégorie

### 3. Gestion des Utilisateurs
1. Aller dans **Authentication and Authorization > Users**
2. Voir le résumé des permissions par utilisateur
3. Assigner des groupes aux utilisateurs
4. Voir les permissions détaillées

### 4. Commandes de Management

#### Configuration initiale
```bash
python manage.py setup_permissions
```

#### Vérification des permissions
```bash
python manage.py shell
>>> from django.contrib.auth.models import Group, Permission
>>> Group.objects.all()
>>> Permission.objects.filter(codename__startswith='commande_')
```

## 📁 Structure des Fichiers

```
apps/
├── users/
│   ├── admin.py                    # Configuration admin personnalisée
│   └── management/
│       └── commands/
│           └── setup_permissions.py # Commande de configuration
├── commande_informatique/
│   └── permissions.py              # Permissions spécifiques
├── commande_bureau/
│   └── permissions.py              # Permissions spécifiques
├── materiel_informatique/
│   └── permissions.py              # Permissions spécifiques
└── materiel_bureautique/
    └── permissions.py              # Permissions spécifiques

templates/
└── admin/
    ├── base_site.html              # Template admin principal
    └── auth/
        └── group/
            └── change_form.html    # Template modification groupes
```

## 🔧 Configuration Avancée

### Ajouter de nouvelles permissions
1. Créer/modifier le fichier `permissions.py` de l'app
2. Ajouter les nouvelles permissions dans la méthode `create_permissions()`
3. Exécuter `python manage.py setup_permissions`

### Exemple d'ajout de permission
```python
# Dans apps/commande_informatique/permissions.py
permissions_commande = [
    # ... permissions existantes ...
    ('custom_action_commande_informatique', 'Peut effectuer une action personnalisée'),
]
```

### Modifier les permissions d'un groupe
1. Aller dans l'admin Django
2. Modifier le groupe concerné
3. Utiliser l'interface organisée par catégories
4. Sauvegarder les modifications

## 🛡️ Sécurité

### Bonnes pratiques
1. **Principe du moindre privilège** : Donner le minimum de permissions nécessaires
2. **Révision régulière** : Vérifier périodiquement les permissions
3. **Audit** : Maintenir des logs des modifications de permissions
4. **Tests** : Tester les permissions avec différents utilisateurs

### Vérification des permissions
```python
# Dans une vue
from django.contrib.auth.decorators import permission_required

@permission_required('commande_informatique.add_commande_informatique')
def ajouter_commande(request):
    # Code de la vue
    pass

# Dans un template
{% if perms.commande_informatique.add_commande_informatique %}
    <a href="{% url 'ajouter_commande' %}">Ajouter une commande</a>
{% endif %}
```

## 📊 Statistiques

### Permissions par groupe
- **Super Admin** : 166 permissions
- **Gestionnaire Informatique** : 19 permissions
- **Gestionnaire Bureau** : 19 permissions
- **Employé** : 8 permissions

### Applications couvertes
- ✅ Commandes Informatiques
- ✅ Commandes Bureau
- ✅ Matériels Informatiques
- ✅ Matériels Bureautiques
- ✅ Fournisseurs
- ✅ Utilisateurs

## 🔄 Maintenance

### Mise à jour des permissions
1. Modifier les fichiers `permissions.py`
2. Exécuter `python manage.py setup_permissions`
3. Vérifier que les groupes ont les bonnes permissions
4. Tester avec différents utilisateurs

### Sauvegarde des configurations
```bash
# Exporter les groupes et permissions
python manage.py dumpdata auth.Group auth.Permission --indent 2 > permissions_backup.json

# Restaurer les groupes et permissions
python manage.py loaddata permissions_backup.json
```

## 📞 Support

Pour toute question concernant la gestion des permissions :
1. Consulter ce document
2. Vérifier les logs Django
3. Tester avec l'utilisateur superadmin
4. Contacter l'administrateur système 