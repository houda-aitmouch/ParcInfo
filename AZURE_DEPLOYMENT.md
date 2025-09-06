# 🚀 Guide de Déploiement Azure for Students - ParcInfo

## 📋 Prérequis
- Compte Azure for Students (avec $100 de crédit)
- Azure CLI installé
- Docker installé
- Projet ParcInfo sur GitHub

## 🎯 Plan de Déploiement

### **Option 1 : Azure App Service (Recommandée)**
- **Service** : Azure App Service (Linux)
- **Base de données** : Azure Database for PostgreSQL
- **Storage** : Azure Storage Account
- **Coût estimé** : ~$20-30/mois

### **Option 2 : Azure Container Instances**
- **Service** : Azure Container Instances
- **Base de données** : Azure Database for PostgreSQL
- **Coût estimé** : ~$15-25/mois

## 🔧 Étapes de Déploiement

### **1. Installation Azure CLI**
```bash
# macOS
brew install azure-cli

# Vérification
az --version
```

### **2. Connexion à Azure**
```bash
# Se connecter à Azure
az login

# Vérifier la connexion
az account show
```

### **3. Créer un groupe de ressources**
```bash
# Créer un groupe de ressources
az group create --name parcinfo-rg --location "West Europe"

# Vérifier la création
az group show --name parcinfo-rg
```

### **4. Créer Azure Database for PostgreSQL**
```bash
# Créer la base de données PostgreSQL
az postgres flexible-server create \
  --resource-group parcinfo-rg \
  --name parcinfo-db \
  --location "West Europe" \
  --admin-user parcinfo_admin \
  --admin-password "ParcInfo2024!" \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --public-access 0.0.0.0-255.255.255.255 \
  --storage-size 32

# Créer la base de données
az postgres flexible-server db create \
  --resource-group parcinfo-rg \
  --server-name parcinfo-db \
  --database-name parcinfo
```

### **5. Créer Azure Container Registry**
```bash
# Créer le registry
az acr create \
  --resource-group parcinfo-rg \
  --name parcinforegistry \
  --sku Basic \
  --admin-enabled true

# Obtenir les identifiants
az acr credential show --name parcinforegistry
```

### **6. Construire et pousser l'image Docker**
```bash
# Se connecter au registry
az acr login --name parcinforegistry

# Construire l'image
docker build -f Dockerfile.azure -t parcinforegistry.azurecr.io/parcinfo:latest .

# Pousser l'image
docker push parcinforegistry.azurecr.io/parcinfo:latest
```

### **7. Créer Azure App Service**
```bash
# Créer le plan App Service
az appservice plan create \
  --resource-group parcinfo-rg \
  --name parcinfo-plan \
  --sku B1 \
  --is-linux

# Créer l'application web
az webapp create \
  --resource-group parcinfo-rg \
  --plan parcinfo-plan \
  --name parcinfo-app \
  --deployment-container-image-name parcinforegistry.azurecr.io/parcinfo:latest
```

### **8. Configurer les variables d'environnement**
```bash
# Configurer les variables
az webapp config appsettings set \
  --resource-group parcinfo-rg \
  --name parcinfo-app \
  --settings \
    DATABASE_URL="postgresql://parcinfo_admin:ParcInfo2024!@parcinfo-db.postgres.database.azure.com:5432/parcinfo" \
    SECRET_KEY="parcinfo-secret-key-2024-azure" \
    DEBUG="False" \
    ALLOWED_HOSTS="*.azurewebsites.net" \
    WEBSITE_SITE_NAME="parcinfo"
```

### **9. Activer les logs**
```bash
# Activer les logs
az webapp log config \
  --resource-group parcinfo-rg \
  --name parcinfo-app \
  --application-logging true \
  --level information
```

## 🌐 Accès à l'Application

### **URL de l'application**
```
https://parcinfo-app.azurewebsites.net
```

### **Admin Django**
```
https://parcinfo-app.azurewebsites.net/admin/
Login: admin
Password: admin123
```

## 💰 Estimation des Coûts

### **Services utilisés :**
- **App Service B1** : ~$13/mois
- **PostgreSQL Flexible Server** : ~$15/mois
- **Container Registry** : ~$5/mois
- **Storage Account** : ~$1/mois
- **Total estimé** : ~$34/mois

### **Avec Azure for Students :**
- **Crédit initial** : $100
- **Durée estimée** : 3-4 mois gratuit

## 🔧 Commandes Utiles

### **Vérifier le statut**
```bash
# Statut de l'application
az webapp show --resource-group parcinfo-rg --name parcinfo-app

# Logs en temps réel
az webapp log tail --resource-group parcinfo-rg --name parcinfo-app
```

### **Redéployer**
```bash
# Redéployer l'image
az webapp restart --resource-group parcinfo-rg --name parcinfo-app
```

### **Mettre à jour l'image**
```bash
# Reconstruire et pousser
docker build -f Dockerfile.azure -t parcinforegistry.azurecr.io/parcinfo:latest .
docker push parcinforegistry.azurecr.io/parcinfo:latest

# Redémarrer l'app
az webapp restart --resource-group parcinfo-rg --name parcinfo-app
```

## 🆘 Dépannage

### **Problèmes courants :**
1. **Erreur de connexion DB** : Vérifier les variables d'environnement
2. **Image trop lourde** : Utiliser Dockerfile.azure optimisé
3. **Timeout de démarrage** : Augmenter le timeout dans les settings

### **Logs de débogage :**
```bash
# Voir les logs
az webapp log tail --resource-group parcinfo-rg --name parcinfo-app

# Télécharger les logs
az webapp log download --resource-group parcinfo-rg --name parcinfo-app
```

## 🎯 Pour votre Soutenance

### **Points à mentionner :**
1. **Déploiement professionnel** sur Azure
2. **Architecture cloud** scalable
3. **Base de données PostgreSQL** gérée
4. **HTTPS automatique** pour la sécurité
5. **Monitoring intégré** avec Azure
6. **Coût optimisé** avec Azure for Students
7. **Déploiement automatique** depuis GitHub

### **URL de démonstration :**
```
https://parcinfo-app.azurewebsites.net
```

---

**🎉 Votre projet ParcInfo sera déployé de manière professionnelle sur Azure !**
