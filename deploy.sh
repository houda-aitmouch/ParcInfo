#!/bin/bash

# Script de déploiement pour ParcInfo
set -e

echo "🚀 Démarrage du déploiement ParcInfo..."

# Vérification des prérequis
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé"
    exit 1
fi

# Arrêt des conteneurs existants
echo "🛑 Arrêt des conteneurs existants..."
docker-compose down --remove-orphans || true

# Nettoyage des images non utilisées
echo "🧹 Nettoyage des images Docker..."
docker system prune -f

# Construction des images
echo "🔨 Construction des images Docker..."
docker-compose build --no-cache

# Démarrage des services
echo "▶️ Démarrage des services..."
docker-compose up -d

# Attente que les services soient prêts
echo "⏳ Attente que les services soient prêts..."
sleep 30

# Vérification du statut des services
echo "🔍 Vérification du statut des services..."
docker-compose ps

# Test de connectivité
echo "🧪 Test de connectivité..."
if curl -f http://localhost:8000/health/ > /dev/null 2>&1; then
    echo "✅ Backend accessible"
else
    echo "❌ Backend non accessible"
fi

if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend accessible"
else
    echo "❌ Frontend non accessible"
fi

echo "🎉 Déploiement terminé!"
echo "📱 Application accessible sur: http://localhost"
echo "🔧 Backend API: http://localhost:8000"
echo "🤖 Chatbot: http://localhost:8001"
