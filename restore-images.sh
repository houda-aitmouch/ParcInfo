#!/bin/bash

# Script de restauration des images Docker ParcInfo
echo "🔄 Restauration des images Docker ParcInfo..."

# Vérifier que le dossier de sauvegarde existe
if [ ! -d "docker-backup" ]; then
    echo "❌ Dossier docker-backup introuvable !"
    echo "💡 Exécutez d'abord : ./save-images.sh"
    exit 1
fi

# Restaurer chaque image
echo "📦 Restauration de parcinfo-backend..."
if [ -f "docker-backup/parcinfo-backend.tar.gz" ]; then
    gunzip -c docker-backup/parcinfo-backend.tar.gz | docker load
    echo "✅ parcinfo-backend restauré"
else
    echo "❌ Fichier parcinfo-backend.tar.gz introuvable"
fi

echo "📦 Restauration de parcinfo-chatbot..."
if [ -f "docker-backup/parcinfo-chatbot.tar.gz" ]; then
    gunzip -c docker-backup/parcinfo-chatbot.tar.gz | docker load
    echo "✅ parcinfo-chatbot restauré"
else
    echo "❌ Fichier parcinfo-chatbot.tar.gz introuvable"
fi

echo "📦 Restauration de parcinfo-frontend..."
if [ -f "docker-backup/parcinfo-frontend.tar.gz" ]; then
    gunzip -c docker-backup/parcinfo-frontend.tar.gz | docker load
    echo "✅ parcinfo-frontend restauré"
else
    echo "❌ Fichier parcinfo-frontend.tar.gz introuvable"
fi

echo "📦 Restauration de postgres:15..."
if [ -f "docker-backup/postgres-15.tar.gz" ]; then
    gunzip -c docker-backup/postgres-15.tar.gz | docker load
    echo "✅ postgres:15 restauré"
else
    echo "❌ Fichier postgres-15.tar.gz introuvable"
fi

echo "📦 Restauration de nginx:alpine..."
if [ -f "docker-backup/nginx-alpine.tar.gz" ]; then
    gunzip -c docker-backup/nginx-alpine.tar.gz | docker load
    echo "✅ nginx:alpine restauré"
else
    echo "❌ Fichier nginx-alpine.tar.gz introuvable"
fi

echo ""
echo "✅ Restauration terminée !"
echo "📋 Images disponibles :"
docker images | grep -E "(parcinfo|postgres|nginx)"
