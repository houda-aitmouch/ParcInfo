# 🚀 Guide de Déploiement Railway Optimisé - ParcInfo

## 📋 Prérequis
- Compte GitHub (déjà configuré)
- Compte Railway (gratuit)
- Projet ParcInfo sur GitHub
- **Contrainte : Image < 4GB**

## 🎯 Déploiement optimisé

### Étape 1 : Créer un compte Railway
1. Aller sur [railway.app](https://railway.app)
2. Cliquer sur "Login with GitHub"
3. Autoriser l'accès à votre compte GitHub

### Étape 2 : Créer un nouveau projet
1. Cliquer sur "New Project"
2. Sélectionner "Deploy from GitHub repo"
3. Choisir le repository `ParcInfo`
4. Cliquer sur "Deploy"

### Étape 3 : Configurer la base de données PostgreSQL
1. Dans le dashboard Railway, cliquer sur "New"
2. Sélectionner "Database" → "PostgreSQL"
3. Attendre que la base soit créée (2-3 minutes)
4. Copier la variable `DATABASE_URL`

### Étape 4 : Configurer les variables d'environnement
Dans le dashboard Railway, aller dans "Variables" et ajouter :

```env
# Base de données
DATABASE_URL=postgresql://user:password@host:port/database

# Django
SECRET_KEY=parcinfo-secret-key-2024-stage-railway
DEBUG=False
ALLOWED_HOSTS=*.railway.app

# Chatbot
HUGGINGFACE_HUB_CACHE=/root/.cache/huggingface
```

### Étape 5 : Déployer
1. Railway détectera automatiquement le `Dockerfile.railway.optimized`
2. Le déploiement commencera automatiquement
3. Attendre 5-10 minutes pour le premier déploiement

### Étape 6 : Accéder à votre application
- URL : `https://votre-projet.railway.app`
- Admin : `https://votre-projet.railway.app/admin/`
- Login : `admin` / `admin123`

## 🔧 Optimisations appliquées

### Image Docker < 4GB
- ✅ **Python 3.11-slim** : Image de base légère
- ✅ **Dépendances optimisées** : Installation minimale
- ✅ **Cache pip purgé** : Réduction de la taille
- ✅ **PyTorch CPU** : Version allégée
- ✅ **Nettoyage APT** : Suppression des caches

### Performance
- ✅ **Gunicorn** : Serveur WSGI optimisé
- ✅ **2 workers** : Équilibrage de charge
- ✅ **Preload** : Chargement optimisé
- ✅ **Limite mémoire** : 2GB max

### Fonctionnalités
- ✅ **Django + Chatbot** : Intégrés dans une seule image
- ✅ **PostgreSQL** : Base de données gérée
- ✅ **HTTPS automatique** : Sécurité maximale
- ✅ **Monitoring** : Logs et métriques

## 🎯 Pour votre Soutenance

### Points à mentionner :
1. **Déploiement professionnel** sur Railway
2. **Image optimisée** < 4GB
3. **HTTPS automatique** pour la sécurité
4. **Base de données PostgreSQL** gérée
5. **Chatbot IA intégré** : Fonctionnel
6. **Monitoring intégré** : Logs et métriques
7. **Déploiement automatique** : Depuis GitHub
8. **Architecture Docker** : Scalable et moderne

### URL de démonstration :
```
https://votre-projet.railway.app
```

## 🆘 Support
- Documentation Railway : [docs.railway.app](https://docs.railway.app)
- Support : [discord.gg/railway](https://discord.gg/railway)

---
**🎉 Votre projet ParcInfo sera déployé de manière professionnelle et optimisée !**
