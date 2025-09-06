#!/bin/bash

# Attendre que la base de données soit prête
echo "Attente de la base de données..."
while ! python -c "import socket; socket.create_connection(('db', 5432))" 2>/dev/null; do
  sleep 1
done
echo "Base de données prête!"

# Configurer CSRF_TRUSTED_ORIGINS
echo "Configuration CSRF_TRUSTED_ORIGINS..."
python -c "
import os
import django
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ParcInfo.settings')
django.setup()
from django.conf import settings
if hasattr(settings, 'CSRF_TRUSTED_ORIGINS'):
    print('CSRF_TRUSTED_ORIGINS already set:', settings.CSRF_TRUSTED_ORIGINS)
else:
    print('CSRF_TRUSTED_ORIGINS not set')
"

# Exécuter les migrations
echo "Exécution des migrations..."
python manage.py migrate --settings=ParcInfo.settings

# Collecter les fichiers statiques
echo "Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --settings=ParcInfo.settings

# Démarrer le serveur Django
echo "Démarrage du serveur Django..."
python manage.py runserver 0.0.0.0:8000 --settings=ParcInfo.settings
