#!/bin/bash

# Script de démarrage Docker pour ParcInfo
# Ce script configure et démarre tous les services Docker

echo "🚀 Démarrage de ParcInfo avec Docker..."

# Vérifier que Docker et Docker Compose sont installés
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez installer Docker d'abord."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Veuillez installer Docker Compose d'abord."
    exit 1
fi

# Vérifier que le fichier env.docker existe
if [ ! -f "env.docker" ]; then
    echo "❌ Le fichier env.docker n'existe pas. Veuillez le créer d'abord."
    exit 1
fi

# Arrêter les conteneurs existants
echo "🛑 Arrêt des conteneurs existants..."
docker-compose down

# Nettoyer les images orphelines (optionnel)
echo "🧹 Nettoyage des images orphelines..."
docker system prune -f

# Construire et démarrer les services
echo "🔨 Construction et démarrage des services..."
docker-compose up --build -d

# Attendre que les services soient prêts
echo "⏳ Attente que les services soient prêts..."
sleep 10

# Vérifier le statut des services
echo "📊 Statut des services:"
docker-compose ps

# Afficher les logs du backend
echo "📝 Logs du backend (dernières 20 lignes):"
docker-compose logs --tail=20 backend

echo ""
echo "✅ ParcInfo est démarré!"
echo "🌐 Accès aux services:"
echo "   - Backend Django: http://localhost:8000"
echo "   - Frontend React: http://localhost:3000"
echo "   - Chatbot: http://localhost:8001"
echo "   - Dashboard Streamlit: http://localhost:8501"
echo "   - Nginx (reverse proxy): http://localhost:80"
echo ""
echo "📋 Commandes utiles:"
echo "   - Voir les logs: docker-compose logs -f [service]"
echo "   - Arrêter: docker-compose down"
echo "   - Redémarrer un service: docker-compose restart [service]"
echo "   - Accéder au shell d'un conteneur: docker-compose exec [service] bash"
