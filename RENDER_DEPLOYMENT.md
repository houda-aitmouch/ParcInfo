# 🚀 Guide de Déploiement Render - ParcInfo

## 📋 Prérequis
- Compte GitHub (déjà configuré)
- Compte Render (gratuit)
- Projet ParcInfo sur GitHub

## 🎯 Déploiement en 1 clic

### Étape 1 : Créer un compte Render
1. Aller sur [render.com](https://render.com)
2. Cliquer sur "Get Started for Free"
3. Se connecter avec GitHub

### Étape 2 : Déployer le backend
1. Cliquer sur "New" → "Web Service"
2. Connecter le repository `ParcInfo`
3. Configurer :
   - **Name** : `parcinfo-backend`
   - **Runtime** : `Python 3`
   - **Build Command** : `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command** : `gunicorn ParcInfo.wsgi:application --bind 0.0.0.0:$PORT`
4. Cliquer sur "Create Web Service"

### Étape 3 : Ajouter PostgreSQL
1. Cliquer sur "New" → "PostgreSQL"
2. Configurer :
   - **Name** : `parcinfo-db`
   - **Plan** : `Free`
3. Cliquer sur "Create Database"

### Étape 4 : Configurer les variables
Dans le service backend, ajouter :
```
SECRET_KEY = parcinfo-secret-key-2024-stage
DEBUG = False
ALLOWED_HOSTS = *.onrender.com
DATABASE_URL = [copier depuis la base de données]
```

### Étape 5 : Déployer le chatbot
1. Cliquer sur "New" → "Web Service"
2. Connecter le même repository `ParcInfo`
3. Configurer :
   - **Name** : `parcinfo-chatbot`
   - **Runtime** : `Python 3`
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `python manage.py runserver 0.0.0.0:$PORT --settings=ParcInfo.settings`
4. Cliquer sur "Create Web Service"

## 🎯 Résultat
- Backend : `https://parcinfo-backend.onrender.com`
- Chatbot : `https://parcinfo-chatbot.onrender.com`
- Admin : `https://parcinfo-backend.onrender.com/admin/`
- Login : `admin` / `admin123`

## ✅ Avantages
- Gratuit 750h/mois
- PostgreSQL inclus
- HTTPS automatique
- Déploiement simple
- Monitoring intégré
