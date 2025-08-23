# Système de Notifications de Garantie

## Vue d'ensemble

Ce système affiche automatiquement des notifications pour tous les équipements dont la garantie expire dans les 30 prochains jours. Les notifications sont filtrées selon le rôle de l'utilisateur connecté.

## Rôles et Permissions

### Super Admin
- **Accès complet** : Voir toutes les notifications de garantie (matériel informatique + matériel bureau)
- **Vue globale** : Accès à l'ensemble du parc informatique

### Gestionnaire Informatique
- **Accès limité** : Seulement les notifications concernant le matériel informatique
- **Focus métier** : Centré sur les équipements IT

### Gestionnaire Bureau
- **Accès limité** : Seulement les notifications concernant le matériel de bureau
- **Focus métier** : Centré sur les équipements bureautiques

## Niveaux d'Urgence

### 🔴 Critique (Rouge)
- **Période** : Garantie expirant dans moins de 7 jours
- **Action requise** : Intervention immédiate
- **Couleur** : Rouge avec bordure rouge

### 🟠 Warning (Orange)
- **Période** : Garantie expirant dans 8-15 jours
- **Action requise** : Planification nécessaire
- **Couleur** : Orange avec bordure orange

### 🔵 Info (Bleu)
- **Période** : Garantie expirant dans 16-30 jours
- **Action requise** : Surveillance
- **Couleur** : Bleu avec bordure bleue

## Fonctionnalités

### Affichage Automatique
- **Chargement** : Au chargement de la page
- **Actualisation** : Toutes les 5 minutes automatiquement
- **Responsive** : S'adapte à la taille de l'écran

### Informations Affichées
- **Équipement** : Désignation et description
- **Identification** : Code d'inventaire et numéro de série (si applicable)
- **Fournisseur** : Nom du fournisseur
- **Commande** : Numéro de commande
- **Utilisateur** : Utilisateur affecté (ou "Non affecté")
- **Statut** : État actuel de l'équipement
- **Temps restant** : Nombre de jours avant expiration
- **Date d'expiration** : Date exacte de fin de garantie

## Architecture Technique

### Backend (Django)
- **Vue** : `apps/users/views.py` - `notifications_garantie()`
- **URL** : `/users/notifications-garantie/`
- **Modèles** : 
  - `MaterielInformatique` (avec propriété `date_fin_garantie_calculee`)
  - `MaterielBureau` (avec propriété `date_fin_garantie_calculee`)

### Frontend (JavaScript)
- **Chargement** : Fetch API vers l'endpoint Django
- **Affichage** : Génération dynamique du HTML
- **Actualisation** : `setInterval` toutes les 5 minutes

### Templates
- **Gestionnaire Info** : `templates/dashboards/base_gestionnaire_info.html`
- **Gestionnaire Bureau** : `templates/dashboards/base_gestionnaire_bureau.html`
- **Super Admin** : `templates/dashboards/base_superadmin.html`

## Installation et Configuration

### 1. Vérifier les Modèles
Assurez-vous que les modèles `MaterielInformatique` et `MaterielBureau` ont la propriété `date_fin_garantie_calculee` qui calcule automatiquement la date de fin de garantie.

### 2. Vérifier les Groupes d'Utilisateurs
Les groupes suivants doivent exister :
- `Super Admin`
- `Gestionnaire Informatique`
- `Gestionnaire Bureau`

### 3. Vérifier les URLs
L'URL `/users/notifications-garantie/` doit être accessible et configurée dans `apps/users/urls.py`.

## Test du Système

### Script de Test
Exécutez le script de test pour vérifier le bon fonctionnement :

```bash
python test_notifications_garantie.py
```

### Test Manuel
1. Connectez-vous avec un utilisateur de chaque rôle
2. Vérifiez que les notifications s'affichent correctement
3. Vérifiez que le filtrage par rôle fonctionne
4. Vérifiez l'actualisation automatique

## Personnalisation

### Modifier la Période d'Alerte
Dans `apps/users/views.py`, modifiez la ligne :
```python
date_limite = timezone.now().date() + timedelta(days=30)
```

### Modifier les Niveaux d'Urgence
Dans les fonctions `get_notifications_materiel_info()` et `get_notifications_materiel_bureau()`, modifiez :
```python
'urgence': 'critique' if jours_restants <= 7 else 'warning' if jours_restants <= 15 else 'info'
```

### Modifier la Fréquence d'Actualisation
Dans les templates, modifiez :
```javascript
setInterval(loadNotificationsGarantie, 5 * 60 * 1000); // 5 minutes
```

## Dépannage

### Problèmes Courants

#### 1. Aucune Notification Affichée
- Vérifiez que les équipements ont des dates de réception
- Vérifiez que la durée de garantie est configurée
- Vérifiez les permissions de l'utilisateur

#### 2. Erreur JavaScript
- Vérifiez la console du navigateur
- Vérifiez que l'URL des notifications est accessible
- Vérifiez l'authentification de l'utilisateur

#### 3. Données Incorrectes
- Vérifiez les propriétés `date_fin_garantie_calculee`
- Vérifiez les relations entre modèles
- Vérifiez les données de test

### Logs et Debug
Activez le mode debug dans Django pour voir les erreurs détaillées :
```python
DEBUG = True
```

## Sécurité

### Authentification
- Toutes les vues de notifications nécessitent une authentification
- Utilisation du décorateur `@login_required`
- Vérification des permissions par groupe

### Autorisation
- Filtrage des données selon le rôle de l'utilisateur
- Pas d'accès aux données d'autres départements
- Validation côté serveur et côté client

## Performance

### Optimisations
- **Requêtes** : Utilisation de `select_related` pour éviter les requêtes N+1
- **Cache** : Actualisation toutes les 5 minutes (configurable)
- **Pagination** : Limitation du nombre de notifications affichées

### Monitoring
- Surveillez les temps de réponse de l'API
- Surveillez l'utilisation mémoire
- Surveillez les requêtes de base de données

## Support et Maintenance

### Mise à Jour
- Vérifiez la compatibilité avec les nouvelles versions de Django
- Testez après chaque modification des modèles
- Sauvegardez avant les modifications importantes

### Documentation
- Maintenez ce README à jour
- Documentez les modifications importantes
- Ajoutez des commentaires dans le code

---

**Note** : Ce système est conçu pour être robuste et maintenable. En cas de problème, consultez d'abord ce README et les logs Django.
