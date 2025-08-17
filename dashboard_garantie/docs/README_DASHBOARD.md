# 🛡️ Dashboard Garantie ParcInfo

Ce dashboard Streamlit permet de visualiser et analyser les durées de garantie des commandes selon les permissions des utilisateurs.

## 🚀 Installation et Lancement

### Méthode 1: Script automatique (Recommandé)
```bash
./launch_dashboard.sh
```

### Méthode 2: Installation manuelle
```bash
# Créer l'environnement virtuel
python3 -m venv env

# Activer l'environnement virtuel
source env/bin/activate  # Sur macOS/Linux
# ou
env\Scripts\activate     # Sur Windows

# Installer les dépendances
pip install -r requirements_streamlit.txt

# Lancer le dashboard
streamlit run dashboard_garantie.py
```

## 🔐 Authentification

Le dashboard utilise l'authentification Django existante :

- **Super Admin**: `superadmin` / `superadmin123` - Accès à toutes les commandes
- **Gestionnaire Informatique**: Accès aux commandes informatiques uniquement
- **Gestionnaire Bureau**: Accès aux commandes bureautiques uniquement
- **Employé**: Accès en lecture seule à toutes les commandes

## 📊 Fonctionnalités

### Selon le rôle de l'utilisateur :

#### 👑 Super Admin
- Vue complète de toutes les commandes (bureautiques et informatiques)
- Métriques globales
- Graphiques de durées de garantie
- Timeline des garanties
- Alertes pour les garanties expirant bientôt

#### 💻 Gestionnaire Informatique
- Vue des commandes informatiques uniquement
- Métriques spécifiques aux commandes informatiques
- Graphiques et analyses détaillées
- Alertes de garantie

#### 📋 Gestionnaire Bureau
- Vue des commandes bureautiques uniquement
- Métriques spécifiques aux commandes bureautiques
- Graphiques et analyses détaillées
- Alertes de garantie

#### 👤 Employé
- Vue en lecture seule de toutes les commandes
- Métriques limitées
- Graphique simple des durées de garantie

## 📈 Visualisations

### Graphiques disponibles :
1. **Barres de durée de garantie** : Affiche les jours restants de garantie par commande
2. **Timeline des garanties** : Représentation temporelle des périodes de garantie
3. **Métriques** : Statistiques clés selon le rôle de l'utilisateur
4. **Alertes** : Notifications pour les garanties expirant dans les 30 prochains jours

## 🗄️ Données affichées

Pour chaque commande :
- Type (Bureautique/Informatique)
- Numéro de commande
- Fournisseur
- Date de commande et réception
- Durée de garantie
- Date de fin de garantie calculée
- Jours restants de garantie
- Statut (En Garantie/Garantie Expirée)

## ⚠️ Prérequis

- Python 3.8+
- Base de données Django configurée et accessible
- Modèles de commandes avec champs de garantie
- Utilisateurs et groupes configurés dans Django

## 🔧 Configuration

Le dashboard se connecte automatiquement à la base de données Django via les paramètres du projet. Assurez-vous que :

1. La base de données est accessible
2. Les migrations Django sont appliquées
3. Les permissions et groupes sont configurés
4. Des données de commandes existent

## 🚨 Dépannage

### Erreur de connexion à la base de données
- Vérifiez que la base de données est accessible
- Vérifiez les paramètres dans `ParcInfo/settings.py`

### Erreur d'import des modèles
- Assurez-vous que Django est correctement configuré
- Vérifiez que les apps sont dans `INSTALLED_APPS`

### Erreur de permissions
- Exécutez la commande de configuration des permissions :
  ```bash
  python manage.py setup_permissions
  ```

## 📝 Personnalisation

Le dashboard peut être personnalisé en modifiant :
- Les couleurs et styles dans le code
- Les seuils d'alerte (actuellement 30 jours)
- Les types de graphiques
- Les métriques affichées

## 🤝 Support

Pour toute question ou problème, consultez la documentation Django et Streamlit ou contactez l'équipe de développement.
