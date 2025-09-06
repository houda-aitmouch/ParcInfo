# 🚀 Guide de Déploiement Heroku - ParcInfo

## 📋 Prérequis
- Compte GitHub (déjà configuré)
- Compte Heroku (gratuit)
- Projet ParcInfo sur GitHub

## 🎯 Déploiement en 1 clic

### Option 1 : Déploiement automatique
1. Aller sur [heroku.com](https://heroku.com)
2. Se connecter avec GitHub
3. Cliquer sur "New" → "Create new app"
4. Nommer l'app : `parcinfo-stage-2024`
5. Cliquer sur "Deploy" → "GitHub"
6. Connecter le repository `ParcInfo`
7. Cliquer sur "Deploy Branch"

### Option 2 : Déploiement manuel
1. Installer Heroku CLI
2. `heroku login`
3. `heroku create parcinfo-stage-2024`
4. `git push heroku main`

## 🔧 Configuration

### Variables d'environnement
```env
SECRET_KEY=parcinfo-secret-key-2024-stage
DEBUG=False
ALLOWED_HOSTS=*.herokuapp.com
```

### Base de données
- PostgreSQL automatiquement ajoutée
- Variable `DATABASE_URL` automatique

## 🎯 Résultat
- URL : `https://parcinfo-stage-2024.herokuapp.com`
- Admin : `https://parcinfo-stage-2024.herokuapp.com/admin/`
- Login : `admin` / `admin123`

## ✅ Avantages
- Gratuit à vie
- HTTPS automatique
- PostgreSQL inclus
- Déploiement simple
- Monitoring intégré
