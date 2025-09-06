#!/bin/bash

echo "🚀 Démarrage complet du projet ParcInfo avec Docker"
echo "=================================================="

# Vérifier que Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez installer Docker d'abord."
    exit 1
fi

# Vérifier que Docker Compose est installé
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Veuillez installer Docker Compose d'abord."
    exit 1
fi

# Arrêter les conteneurs existants
echo "🛑 Arrêt des conteneurs existants..."
docker-compose down

# Nettoyer les images et volumes (optionnel)
read -p "Voulez-vous nettoyer les images et volumes existants ? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧹 Nettoyage des images et volumes..."
    docker-compose down -v --rmi all
    docker system prune -f
fi

# Construire les images
echo "🔨 Construction des images Docker..."
docker-compose build --no-cache

# Démarrer les services
echo "🚀 Démarrage des services..."
docker-compose up -d

# Attendre que les services soient prêts
echo "⏳ Attente que les services soient prêts..."
sleep 30

# Vérifier le statut des services
echo "📊 Statut des services:"
docker-compose ps

# Afficher les logs
echo "📝 Logs des services:"
docker-compose logs --tail=50

echo ""
echo "✅ Démarrage terminé !"
echo ""
echo "🌐 Services disponibles:"
echo "  - Backend Django: http://localhost:8000"
echo "  - Frontend React: http://localhost:3000"
echo "  - Chatbot: http://localhost:8001"
echo "  - Streamlit Dashboard: http://localhost:8501"
echo "  - Nginx (proxy): http://localhost:80"
echo ""
echo "📋 Commandes utiles:"
echo "  - Voir les logs: docker-compose logs -f"
echo "  - Arrêter: docker-compose down"
echo "  - Redémarrer: docker-compose restart"
echo "  - Accéder à un conteneur: docker-compose exec <service> bash"
