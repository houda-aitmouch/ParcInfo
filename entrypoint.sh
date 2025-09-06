#!/bin/bash

# Attendre que la base de données soit prête
echo "Attente de la base de données..."
while ! python -c "import socket; socket.create_connection(('db', 5432))" 2>/dev/null; do
  sleep 1
done
echo "Base de données prête!"

# Exécuter les migrations
echo "Exécution des migrations..."
python manage.py migrate --settings=ParcInfo.settings

# Collecter les fichiers statiques
echo "Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --settings=ParcInfo.settings

# Créer un superutilisateur si nécessaire
echo "Création du superutilisateur..."
python manage.py shell --settings=ParcInfo.settings << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@parcinfo.com', 'admin123')
    print('Superutilisateur créé: admin/admin123')
else:
    print('Superutilisateur existe déjà')
EOF

# Démarrer le serveur Django
echo "Démarrage du serveur Django..."
exec python manage.py runserver 0.0.0.0:8000 --settings=ParcInfo.settings