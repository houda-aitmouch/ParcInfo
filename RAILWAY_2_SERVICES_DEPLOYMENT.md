# 🚀 Guide de Déploiement Railway - 2 Services Séparés

## 📋 Prérequis
- Compte GitHub (déjà configuré)
- Compte Railway (gratuit)
- Projet ParcInfo sur GitHub
- **Contrainte : Chaque image < 4GB**

## 🎯 Architecture de Déploiement

### **Service 1 : Backend Django**
- **Dockerfile** : `Dockerfile.railway.backend-only`
- **Port** : 8000
- **Fonctionnalités** : Django, PostgreSQL, Admin, API
- **Taille** : < 4GB

### **Service 2 : Chatbot IA**
- **Dockerfile** : `Dockerfile.railway.chatbot-only`
- **Port** : 8001
- **Fonctionnalités** : Chatbot, Modèles IA, API Chatbot
- **Taille** : < 4GB

## 🎯 Déploiement en 2 étapes

### **ÉTAPE 1 : Créer le projet principal**
1. Aller sur [railway.app](https://railway.app)
2. Cliquer sur "Login with GitHub"
3. Cliquer sur "New Project"
4. Sélectionner "Deploy from GitHub repo"
5. Choisir le repository `ParcInfo`
6. Cliquer sur "Deploy"

### **ÉTAPE 2 : Ajouter PostgreSQL**
1. Dans le dashboard Railway, cliquer sur "New"
2. Sélectionner "Database" → "PostgreSQL"
3. Attendre que la base soit créée (2-3 minutes)
4. Copier la variable `DATABASE_URL`

### **ÉTAPE 3 : Configurer le Backend (Service 1)**
1. Dans le projet principal, cliquer sur "Settings"
2. Aller dans "Deploy"
3. Changer le Dockerfile vers `Dockerfile.railway.backend-only`
4. Configurer les variables d'environnement :
   ```env
   DATABASE_URL=postgresql://user:password@host:port/database
   SECRET_KEY=parcinfo-secret-key-2024-stage-railway
   DEBUG=False
   ALLOWED_HOSTS=*.railway.app
   ```

### **ÉTAPE 4 : Créer le Chatbot (Service 2)**
1. Cliquer sur "New" → "Service"
2. Sélectionner "Deploy from GitHub repo"
3. Choisir le même repository `ParcInfo`
4. Changer le Dockerfile vers `Dockerfile.railway.chatbot-only`
5. Configurer les variables d'environnement :
   ```env
   DATABASE_URL=postgresql://user:password@host:port/database
   SECRET_KEY=parcinfo-secret-key-2024-stage-railway
   DEBUG=False
   ALLOWED_HOSTS=*.railway.app
   HUGGINGFACE_HUB_CACHE=/root/.cache/huggingface
   ```

### **ÉTAPE 5 : Déployer les deux services**
1. Les deux services se déploieront automatiquement
2. Attendre 5-10 minutes pour le premier déploiement
3. Vérifier que les deux services sont "Running"

## 🎯 Résultat

### **URLs d'accès :**
- **Backend** : `https://votre-projet-backend.railway.app`
- **Chatbot** : `https://votre-projet-chatbot.railway.app`
- **Admin** : `https://votre-projet-backend.railway.app/admin/`
- **API Chatbot** : `https://votre-projet-chatbot.railway.app/chatbot/api/`

### **Login :**
- **Username** : `admin`
- **Password** : `admin123`

## 🔧 Avantages de cette architecture

### **Respect des contraintes :**
- ✅ **Chaque image < 4GB** : Respect de la limite Railway
- ✅ **Chatbot fonctionnel** : Modèles IA inclus
- ✅ **Backend complet** : Django + PostgreSQL
- ✅ **Séparation des responsabilités** : Services indépendants

### **Performance :**
- ✅ **Déploiement parallèle** : Les deux services se déploient en même temps
- ✅ **Scalabilité** : Chaque service peut être mis à l'échelle indépendamment
- ✅ **Maintenance** : Mise à jour d'un service sans affecter l'autre

### **Monitoring :**
- ✅ **Logs séparés** : Chaque service a ses propres logs
- ✅ **Métriques individuelles** : Performance de chaque service
- ✅ **Débogage facilité** : Problèmes isolés par service

## 🎯 Pour votre Soutenance

### **Points à mentionner :**
1. **Architecture microservices** : Services séparés et indépendants
2. **Respect des contraintes** : Images < 4GB chacune
3. **Chatbot IA fonctionnel** : Modèles IA inclus
4. **Backend complet** : Django + PostgreSQL
5. **Déploiement professionnel** : Railway avec HTTPS
6. **Scalabilité** : Services indépendants et évolutifs

### **URLs de démonstration :**
```
Backend: https://votre-projet-backend.railway.app
Chatbot: https://votre-projet-chatbot.railway.app
```

## 🆘 Support
- Documentation Railway : [docs.railway.app](https://docs.railway.app)
- Support : [discord.gg/railway](https://discord.gg/railway)

---
**🎉 Votre projet ParcInfo sera déployé avec le chatbot fonctionnel !**
