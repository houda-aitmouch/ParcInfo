#!/bin/bash

# Script de démarrage Railway
echo "🚀 Démarrage de ParcInfo sur Railway..."

# Attendre que la base de données soit prête
echo "⏳ Attente de la base de données..."
while ! python -c "import socket; socket.create_connection(('$DATABASE_HOST', $DATABASE_PORT))" 2>/dev/null; do
    sleep 1
done

echo "✅ Base de données connectée"

# Migrations
echo "🔄 Exécution des migrations..."
python manage.py migrate --settings=ParcInfo.settings

# Collecte des fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --settings=ParcInfo.settings

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

# Démarrage de Nginx en arrière-plan
echo "🌐 Démarrage de Nginx..."
nginx -g "daemon off;" &

# Démarrage de Django
echo "🐍 Démarrage de Django..."
python manage.py runserver 0.0.0.0:8001 --settings=ParcInfo.settings

echo "✅ ParcInfo démarré avec succès sur Railway!"
