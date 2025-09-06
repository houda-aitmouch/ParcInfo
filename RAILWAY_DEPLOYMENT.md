# 🚀 Guide de Déploiement Railway - ParcInfo

## 📋 Prérequis
- Compte GitHub (déjà configuré)
- Compte Railway (gratuit)
- Projet ParcInfo sur GitHub

## 🎯 Étapes de Déploiement

### 1. Créer un compte Railway
1. Aller sur [railway.app](https://railway.app)
2. Cliquer sur "Login with GitHub"
3. Autoriser l'accès à votre compte GitHub

### 2. Créer un nouveau projet
1. Cliquer sur "New Project"
2. Sélectionner "Deploy from GitHub repo"
3. Choisir le repository `ParcInfo`
4. Cliquer sur "Deploy"

### 3. Configurer la base de données PostgreSQL
1. Dans le dashboard Railway, cliquer sur "New"
2. Sélectionner "Database" → "PostgreSQL"
3. Attendre que la base soit créée
4. Copier les variables de connexion :
   - `DATABASE_URL`
   - `PGHOST`
   - `PGPORT`
   - `PGUSER`
   - `PGPASSWORD`
   - `PGDATABASE`

### 4. Configurer les variables d'environnement
Dans le dashboard Railway, aller dans "Variables" et ajouter :

```env
# Base de données
DATABASE_URL=postgresql://user:password@host:port/database
DATABASE_HOST=host
DATABASE_PORT=5432
DATABASE_NAME=database
DATABASE_USER=user
DATABASE_PASSWORD=password

# Django
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=*.railway.app

# Chatbot
HUGGINGFACE_HUB_CACHE=/root/.cache/huggingface
```

### 5. Déployer
1. Railway détectera automatiquement le `Dockerfile.railway`
2. Le déploiement commencera automatiquement
3. Attendre 5-10 minutes pour le premier déploiement

### 6. Accéder à votre application
- URL : `https://votre-projet.railway.app`
- Admin : `https://votre-projet.railway.app/admin/`
- Login : `admin` / `admin123`

## 🔧 Configuration Avancée

### Monitoring
- Logs en temps réel dans le dashboard Railway
- Métriques de performance
- Alertes automatiques

### Déploiement automatique
- Chaque push sur `main` déclenche un redéploiement
- Tests automatiques avant déploiement
- Rollback en un clic

### HTTPS
- Certificat SSL automatique
- Redirection HTTP → HTTPS
- Sécurité maximale

## 🎯 Pour votre Soutenance

### Points à mentionner :
1. **Déploiement professionnel** sur Railway
2. **HTTPS automatique** pour la sécurité
3. **Base de données PostgreSQL** gérée
4. **Monitoring intégré** pour la maintenance
5. **Déploiement automatique** depuis GitHub
6. **Architecture Docker** pour la scalabilité

### URL de démonstration :
```
https://votre-projet.railway.app
```

## 🆘 Support
- Documentation Railway : [docs.railway.app](https://docs.railway.app)
- Support : [discord.gg/railway](https://discord.gg/railway)

---
**🎉 Votre projet ParcInfo sera déployé de manière professionnelle et gratuite !**
