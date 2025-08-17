# 🚀 Guide de Lancement du Projet ParcInfo

Ce guide explique comment lancer automatiquement Django et Streamlit simultanément.

## 📋 Prérequis

- Python 3.8+ installé
- Toutes les dépendances installées (`pip install -r requirements.txt`)
- Base de données Django configurée et migrée

## 🎯 Lancement Automatique

### Sur macOS/Linux

```bash
./launch_project.sh
```

### Sur Windows

```cmd
launch_project.bat
```

## 🔧 Fonctionnalités des Scripts

### ✅ Vérifications Automatiques
- Vérification de la disponibilité des ports (8000 et 8501)
- Arrêt automatique des processus existants si nécessaire
- Test de connectivité des serveurs après démarrage

### 🌐 Serveurs Lancés
- **Django** : http://localhost:8000
- **Streamlit Dashboard** : http://localhost:8501

### 🛑 Arrêt des Serveurs

#### Sur macOS/Linux
- Appuyez sur `Ctrl+C` dans le terminal où le script est lancé
- Ou utilisez : `pkill -f "python manage.py runserver"` et `pkill -f "streamlit run dashboard_garantie.py"`

#### Sur Windows
- Fermez les fenêtres de terminal ouvertes par le script
- Ou utilisez le Gestionnaire des tâches pour arrêter les processus Python

## 📊 Accès au Dashboard

1. **Connectez-vous à Django** : http://localhost:8000
2. **Accédez au dashboard** via les liens dans les dashboards utilisateur
3. **Ou accédez directement** : http://localhost:8501

## 🔍 Dépannage

### Ports déjà utilisés
Les scripts arrêtent automatiquement les processus existants. Si cela ne fonctionne pas :

```bash
# macOS/Linux
lsof -ti:8000 | xargs kill -9
lsof -ti:8501 | xargs kill -9

# Windows
netstat -ano | findstr :8000
netstat -ano | findstr :8501
# Puis utilisez taskkill avec le PID trouvé
```

### Erreurs de dépendances
```bash
pip install -r requirements.txt
pip install -r dashboard_garantie/requirements_streamlit.txt
```

### Problèmes de base de données
```bash
python manage.py makemigrations
python manage.py migrate
```

## 📝 Logs

Les logs des serveurs s'affichent dans les terminaux correspondants :
- Django : Terminal principal
- Streamlit : Fenêtre séparée (Windows) ou arrière-plan (macOS/Linux)

## 🎉 Avantages

- ✅ Lancement en un seul clic
- ✅ Gestion automatique des ports
- ✅ Arrêt propre des serveurs
- ✅ Vérification de l'état des services
- ✅ Compatible macOS/Linux/Windows

---

**Note** : Les scripts sont configurés pour les chemins spécifiques du projet. Si vous déplacez le projet, mettez à jour les chemins dans les scripts.
