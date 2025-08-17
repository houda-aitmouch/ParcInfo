# 🛡️ Dashboard Garantie ParcInfo

Dashboard Streamlit pour la gestion et le suivi des garanties des commandes selon les permissions des utilisateurs.

## 📁 Structure du Projet

```
dashboard_garantie/
├── dashboard_garantie.py          # Dashboard principal
├── run_dashboard.py               # Script de lancement principal
├── requirements_streamlit.txt     # Dépendances spécifiques
├── scripts/                       # Scripts utilitaires
│   ├── launch_dashboard.sh        # Lancement Linux/macOS
│   ├── launch_dashboard.bat       # Lancement Windows
│   ├── install_dependencies.sh    # Installation dépendances
│   ├── test_dashboard.py          # Test de configuration
│   ├── demo_data.py               # Données de démonstration
│   └── create_users.py            # Création d'utilisateurs
├── config/                        # Configuration
│   ├── .streamlit/                # Configuration Streamlit
│   └── env_config.example         # Variables d'environnement
└── docs/                          # Documentation
    ├── README_DASHBOARD.md        # Documentation complète
    └── QUICKSTART.md              # Guide de démarrage rapide
```

## 🚀 Démarrage Rapide

### Depuis le dossier racine du projet :

```bash
# Configuration complète (recommandé)
python dashboard_garantie/run_dashboard.py --setup

# Ou étape par étape :
python dashboard_garantie/run_dashboard.py --install  # Installer dépendances
python dashboard_garantie/run_dashboard.py --users    # Créer utilisateurs
python dashboard_garantie/run_dashboard.py --data     # Créer données de test
python dashboard_garantie/run_dashboard.py            # Lancer le dashboard
```

### Depuis le dossier dashboard_garantie :

```bash
# Installation
./scripts/install_dependencies.sh

# Test
python scripts/test_dashboard.py

# Lancement
./scripts/launch_dashboard.sh
```

## 🔐 Utilisateurs de Test

| Rôle | Username | Mot de passe | Accès |
|------|----------|--------------|-------|
| 👑 Super Admin | `superadmin` | `superadmin123` | Toutes les commandes |
| 👑 Admin Garantie | `admin_garantie` | `admingarantie123` | Toutes les commandes |
| 💻 Gestionnaire Info | `gest_info` | `gestinfo123` | Commandes informatiques |
| 📋 Gestionnaire Bureau | `gest_bureau` | `gestbureau123` | Commandes bureautiques |
| 👤 Employé 1 | `employe1` | `employe123` | Lecture seule |
| 👤 Employé 2 | `employe2` | `employe123` | Lecture seule |

## 📊 Fonctionnalités

### Selon le rôle de l'utilisateur :

- **👑 Super Admin** : Vue complète avec toutes les commandes
- **💻 Gestionnaire Informatique** : Commandes informatiques uniquement
- **📋 Gestionnaire Bureau** : Commandes bureautiques uniquement
- **👤 Employé** : Vue en lecture seule de toutes les commandes

### Visualisations disponibles :

- 📈 **Métriques en temps réel** : Statistiques selon le rôle
- 📊 **Graphiques de garantie** : Durées restantes par commande
- 📅 **Timeline des garanties** : Représentation temporelle
- 🚨 **Alertes** : Garanties expirant dans les 30 prochains jours

## 🔧 Configuration

### Prérequis :

- Python 3.8+
- Django configuré avec base de données
- Permissions et groupes configurés
- Environnement virtuel activé

### Variables d'environnement :

Copiez `config/env_config.example` vers `.env` et configurez :

```bash
DJANGO_SETTINGS_MODULE=ParcInfo.settings
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

## 📋 Commandes Utiles

### Script principal (`run_dashboard.py`) :

```bash
python dashboard_garantie/run_dashboard.py --help     # Aide
python dashboard_garantie/run_dashboard.py --setup    # Configuration complète
python dashboard_garantie/run_dashboard.py --install  # Installer dépendances
python dashboard_garantie/run_dashboard.py --test     # Tester configuration
python dashboard_garantie/run_dashboard.py --users    # Créer utilisateurs
python dashboard_garantie/run_dashboard.py --data     # Créer données de test
```

### Scripts individuels :

```bash
# Création d'utilisateurs
python dashboard_garantie/scripts/create_users.py
python dashboard_garantie/scripts/create_users.py --list
python dashboard_garantie/scripts/create_users.py --delete

# Données de démonstration
python dashboard_garantie/scripts/demo_data.py
python dashboard_garantie/scripts/demo_data.py --cleanup

# Test de configuration
python dashboard_garantie/scripts/test_dashboard.py
```

## 🌐 Accès

Une fois lancé, le dashboard est accessible à :
```
http://localhost:8501
```

## 🚨 Dépannage

### Erreurs courantes :

1. **ModuleNotFoundError** : Installez les dépendances avec `--install`
2. **Erreur de base de données** : Vérifiez la configuration Django
3. **Erreur de permissions** : Exécutez `python manage.py setup_permissions`
4. **Port déjà utilisé** : Changez le port dans la configuration

### Logs et débogage :

- Vérifiez les messages dans le terminal
- Consultez `docs/README_DASHBOARD.md` pour plus de détails
- Utilisez `--test` pour diagnostiquer les problèmes

## 📝 Personnalisation

Le dashboard peut être personnalisé en modifiant :

- **Couleurs et thème** : `config/.streamlit/config.toml`
- **Seuils d'alerte** : Dans `dashboard_garantie.py`
- **Types de graphiques** : Fonctions dans `dashboard_garantie.py`
- **Métriques affichées** : Selon le rôle dans `dashboard_garantie.py`

## 🤝 Support

- 📖 **Documentation complète** : `docs/README_DASHBOARD.md`
- 🚀 **Guide de démarrage** : `docs/QUICKSTART.md`
- 🧪 **Tests** : `scripts/test_dashboard.py`
- 💡 **Exemples** : `scripts/demo_data.py`

## 📄 Licence

Ce dashboard fait partie du projet ParcInfo et suit les mêmes conditions d'utilisation.
