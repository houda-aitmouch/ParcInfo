# 🚀 Guide de Déploiement DigitalOcean - ParcInfo

## 📋 Prérequis
- Compte GitHub (déjà configuré)
- Compte DigitalOcean (gratuit avec $200 de crédit)
- Projet ParcInfo sur GitHub

## 🎯 Déploiement professionnel

### Étape 1 : Créer un compte DigitalOcean
1. Aller sur [digitalocean.com](https://digitalocean.com)
2. Cliquer sur "Sign Up"
3. Utiliser le code promo pour $200 de crédit gratuit

### Étape 2 : Créer une App Platform
1. Aller dans "App Platform"
2. Cliquer sur "Create App"
3. Connecter le repository `ParcInfo`

### Étape 3 : Configurer les services
1. **Backend Django** :
   - Type : Web Service
   - Source : GitHub
   - Build Command : `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Run Command : `gunicorn ParcInfo.wsgi:application --bind 0.0.0.0:$PORT`

2. **Chatbot** :
   - Type : Web Service
   - Source : GitHub
   - Build Command : `pip install -r requirements.txt`
   - Run Command : `python manage.py runserver 0.0.0.0:$PORT --settings=ParcInfo.settings`

3. **PostgreSQL** :
   - Type : Database
   - Plan : Basic ($15/mois)

### Étape 4 : Configurer les variables
```
SECRET_KEY = parcinfo-secret-key-2024-stage
DEBUG = False
ALLOWED_HOSTS = *.ondigitalocean.app
DATABASE_URL = [automatique]
```

## 🎯 Résultat
- URL : `https://votre-app.ondigitalocean.app`
- Admin : `https://votre-app.ondigitalocean.app/admin/`
- Login : `admin` / `admin123`

## ✅ Avantages
- Très professionnel
- $200 de crédit gratuit
- PostgreSQL géré
- HTTPS automatique
- Monitoring avancé
- Support 24/7

## 💰 Coût
- App Platform : $5/mois
- PostgreSQL : $15/mois
- Total : $20/mois (gratuit avec crédit)
