#!/bin/bash

# Script de déploiement ParcInfo
echo "🚀 Déploiement ParcInfo - Images Docker Prêtes"

# Vérifier que Docker est en cours d'exécution
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker n'est pas en cours d'exécution. Veuillez démarrer Docker Desktop."
    exit 1
fi

# Vérifier les images disponibles
echo "📋 Images Docker disponibles :"
docker images | grep parcinfo

echo ""
echo "🎯 Options de déploiement :"
echo "1. Démarrage local (Docker Compose)"
echo "2. Déploiement Azure"
echo "3. Déploiement Railway"
echo "4. Voir les logs"
echo "5. Arrêter les services"

read -p "Choisissez une option (1-5) : " choice

case $choice in
    1)
        echo "🐳 Démarrage local avec Docker Compose..."
        docker-compose up -d
        echo "✅ Services démarrés !"
        echo "🌐 Application : http://localhost:8000"
        echo "👤 Admin : http://localhost:8000/admin/ (admin/admin123)"
        ;;
    2)
        echo "☁️ Déploiement Azure..."
        echo "📋 Étapes :"
        echo "1. Se connecter à Azure : az login"
        echo "2. Créer le groupe de ressources : az group create --name parcinfo-rg --location 'West Europe'"
        echo "3. Créer la base de données : az postgres flexible-server create --resource-group parcinfo-rg --name parcinfo-db --location 'West Europe' --admin-user parcinfo_admin --admin-password 'ParcInfo2024!' --sku-name Standard_B1ms --tier Burstable --public-access 0.0.0.0-255.255.255.255 --storage-size 32"
        echo "4. Suivre le guide : AZURE_DEPLOYMENT.md"
        ;;
    3)
        echo "🚂 Déploiement Railway..."
        echo "📋 Étapes :"
        echo "1. Aller sur railway.app"
        echo "2. Se connecter avec GitHub"
        echo "3. Sélectionner le repository ParcInfo"
        echo "4. Railway détectera automatiquement le Dockerfile"
        echo "5. Configurer les variables d'environnement"
        ;;
    4)
        echo "📊 Logs des services :"
        docker-compose logs -f
        ;;
    5)
        echo "🛑 Arrêt des services..."
        docker-compose down
        echo "✅ Services arrêtés !"
        ;;
    *)
        echo "❌ Option invalide"
        ;;
esac

echo ""
echo "📚 Documentation complète :"
echo "- DOCKER_IMAGES.md : Guide des images Docker"
echo "- AZURE_DEPLOYMENT.md : Déploiement Azure"
echo "- RAILWAY_OPTIMIZED_DEPLOYMENT.md : Déploiement Railway"
echo ""
echo "🎉 ParcInfo est prêt pour le déploiement !"