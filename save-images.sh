#!/bin/bash

# Script de sauvegarde des images Docker ParcInfo
echo "💾 Sauvegarde des images Docker ParcInfo..."

# Créer le dossier de sauvegarde
mkdir -p docker-backup

# Sauvegarder chaque image
echo "📦 Sauvegarde de parcinfo-backend..."
docker save parcinfo-backend:latest | gzip > docker-backup/parcinfo-backend.tar.gz

echo "📦 Sauvegarde de parcinfo-chatbot..."
docker save parcinfo-chatbot:latest | gzip > docker-backup/parcinfo-chatbot.tar.gz

echo "📦 Sauvegarde de parcinfo-frontend..."
docker save parcinfo-frontend:latest | gzip > docker-backup/parcinfo-frontend.tar.gz

echo "📦 Sauvegarde de postgres:15..."
docker save postgres:15 | gzip > docker-backup/postgres-15.tar.gz

echo "📦 Sauvegarde de nginx:alpine..."
docker save nginx:alpine | gzip > docker-backup/nginx-alpine.tar.gz

echo "✅ Sauvegarde terminée !"
echo "📁 Fichiers sauvegardés dans : docker-backup/"
ls -lh docker-backup/

echo ""
echo "🔄 Pour restaurer les images :"
echo "gunzip -c docker-backup/parcinfo-backend.tar.gz | docker load"
echo "gunzip -c docker-backup/parcinfo-chatbot.tar.gz | docker load"
echo "gunzip -c docker-backup/parcinfo-frontend.tar.gz | docker load"
echo "gunzip -c docker-backup/postgres-15.tar.gz | docker load"
echo "gunzip -c docker-backup/nginx-alpine.tar.gz | docker load"
