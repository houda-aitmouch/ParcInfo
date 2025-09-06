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

# Vérifier l'existence du superutilisateur
echo "Vérification du superutilisateur..."
python manage.py shell --settings=ParcInfo.settings << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if User.objects.filter(username='admin').exists():
    print('Superutilisateur admin existe déjà')
else:
    print('Aucun superutilisateur trouvé - veuillez en créer un manuellement')
EOF

# Démarrer le serveur Django
echo "Démarrage du serveur Django..."
exec python manage.py runserver 0.0.0.0:8000 --settings=ParcInfo.settings