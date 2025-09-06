#!/bin/bash

# Script de démarrage Railway - Chatbot seul
echo "🚀 Démarrage de ParcInfo Chatbot sur Railway..."

# Attendre que la base de données soit prête
echo "⏳ Attente de la base de données..."
while ! python -c "import socket; socket.create_connection(('$DATABASE_HOST', $DATABASE_PORT))" 2>/dev/null; do
    sleep 1
done

echo "✅ Base de données connectée"

# Migrations
echo "🔄 Exécution des migrations..."
python manage.py migrate --settings=ParcInfo.settings

# Démarrage de Django avec Gunicorn (chatbot)
echo "🤖 Démarrage de Django Chatbot avec Gunicorn..."
gunicorn ParcInfo.wsgi:application \
    --bind 0.0.0.0:8001 \
    --workers 1 \
    --worker-class sync \
    --worker-connections 1000 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --timeout 30 \
    --keep-alive 2 \
    --preload \
    --log-level info

echo "✅ ParcInfo Chatbot démarré avec succès sur Railway!"
