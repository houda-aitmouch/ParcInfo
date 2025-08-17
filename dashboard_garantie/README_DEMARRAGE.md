# 🚀 Guide de Démarrage du Dashboard de Garanties ParcInfo

## 📋 Prérequis

- Python 3.8+ installé
- Streamlit installé (`pip install streamlit`)
- Django configuré et fonctionnel
- Accès aux modèles de base de données ParcInfo

## 🎯 Démarrage Rapide

### Option 1: Script Automatique (Recommandé)

#### Sur macOS/Linux :
```bash
cd dashboard_garantie
./start_dashboard.sh
```

#### Sur Windows :
```cmd
cd dashboard_garantie
start_dashboard.bat
```

### Option 2: Commande Manuelle

```bash
cd dashboard_garantie
python -m streamlit run dashboard_garantie.py --server.port 8501
```

## 🌐 Accès au Dashboard

- **URL locale** : http://localhost:8501
- **URL réseau** : http://[VOTRE_IP]:8501

## 🔧 Configuration des Ports

### Port par défaut : 8501
Le dashboard utilise le port 8501 par défaut pour être compatible avec Django.

### Changer le port :
```bash
# Sur macOS/Linux
./start_dashboard.sh 8502

# Sur Windows
start_dashboard.bat 8502

# Commande manuelle
python -m streamlit run dashboard_garantie.py --server.port 8502
```

## 🚨 Résolution des Problèmes

### Erreur "Connection refused" sur le port 8501
```bash
# Vérifier si le port est utilisé
lsof -i :8501

# Arrêter le processus existant
pkill -f "streamlit run dashboard_garantie.py"

# Redémarrer
./start_dashboard.sh
```

### Erreur "Port already in use"
Le script de démarrage automatique gère cette situation et arrête le processus existant.

### Erreur "Module not found"
```bash
# Installer les dépendances
pip install -r requirements.txt

# Ou installer Streamlit directement
pip install streamlit
```

## 📱 Accès depuis Django

Le dashboard est accessible depuis l'interface Django via :
- **Super Admin** : Dashboard principal avec toutes les garanties
- **Gestionnaire Informatique** : Garanties des équipements informatiques
- **Gestionnaire Bureau** : Garanties des équipements bureautiques

## 🔒 Sécurité

- Seuls les utilisateurs autorisés peuvent accéder au dashboard
- Authentification automatique via Django
- Rôles et permissions respectés

## 📊 Fonctionnalités

- **Timeline des garanties** : Visualisation temporelle
- **Analyse par fournisseur** : Statistiques et graphiques
- **Filtres avancés** : Par statut, type, fournisseur
- **Tri intelligent** : Par jours restants, dates, etc.
- **Interface responsive** : Compatible mobile et desktop

## 🛠️ Maintenance

### Scripts disponibles
- **`start_dashboard.sh`** : Démarrage automatique avec gestion des conflits
- **`check_status.sh`** : Vérification complète de l'état du dashboard
- **`start_dashboard.bat`** : Version Windows du script de démarrage

### Arrêter le serveur
```bash
# Arrêt manuel
Ctrl+C

# Ou arrêt forcé
pkill -f "streamlit run dashboard_garantie.py"
```

### Redémarrer
```bash
./start_dashboard.sh
```

### Vérifier l'état
```bash
./check_status.sh
```

### Logs
Les logs sont affichés dans le terminal où le serveur a été démarré.

## 📞 Support

En cas de problème :
1. Vérifier que le port 8501 est libre
2. Redémarrer le serveur avec le script automatique
3. Vérifier les logs d'erreur dans le terminal
4. Contacter l'administrateur système

---

**Note** : Le dashboard doit être démarré AVANT d'accéder aux pages Django qui y font référence.
