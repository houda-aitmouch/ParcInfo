#!/bin/bash

# Script de démarrage Railway EXTREME-optimisé
echo "🚀 Démarrage de ParcInfo sur Railway (EXTREME-optimisé)..."

# Attendre que la base de données soit prête
echo "⏳ Attente de la base de données..."
while ! python -c "import socket; socket.create_connection(('$DATABASE_HOST', $DATABASE_PORT))" 2>/dev/null; do
    sleep 1
done

echo "✅ Base de données connectée"

# Migrations
echo "🔄 Exécution des migrations..."
python manage.py migrate --settings=ParcInfo.settings

# Création du superutilisateur si nécessaire
echo "👤 Vérification du superutilisateur..."
python manage.py shell --settings=ParcInfo.settings << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@parcinfo.com', 'admin123')
    print('Superutilisateur admin créé')
else:
    print('Superutilisateur admin existe déjà')
EOF

# Démarrage de Django avec Gunicorn (EXTREME-optimisé)
echo "🐍 Démarrage de Django avec Gunicorn..."
gunicorn ParcInfo.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 1 \
    --worker-class sync \
    --worker-connections 1000 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --timeout 30 \
    --keep-alive 2 \
    --preload \
    --log-level warning

echo "✅ ParcInfo démarré avec succès sur Railway!"
