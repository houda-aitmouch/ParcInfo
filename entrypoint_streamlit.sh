#!/bin/bash

# Charger les variables d'environnement depuis le fichier .env
if [ -f /app/.env ]; then
    echo "Chargement des variables d'environnement depuis .env..."
    export $(cat /app/.env | grep -v '^#' | xargs)
fi

# Attendre que la base de données soit prête
echo "Attente de la base de données sur ${DB_HOST:-host.docker.internal}:${DB_PORT:-5432}..."
while ! python -c "import socket; socket.create_connection(('${DB_HOST:-host.docker.internal}', ${DB_PORT:-5432}))" 2>/dev/null; do
  sleep 1
done
echo "Base de données prête!"

# Vérifier la configuration
echo "Configuration actuelle:"
echo "DEBUG: ${DEBUG:-0}"
echo "DB_HOST: ${DB_HOST:-host.docker.internal}"
echo "DB_NAME: ${DB_NAME:-parcinfo_db}"
echo "DB_USER: ${DB_USER:-Houda}"

# Exécuter les migrations
echo "Exécution des migrations..."
python manage.py migrate --settings=ParcInfo.settings

# Collecter les fichiers statiques
echo "Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --settings=ParcInfo.settings

# Démarrer Streamlit
echo "Démarrage de Streamlit..."
cd /app/dashboard_garantie
streamlit run dashboard_garantie.py --server.port=8501 --server.address=0.0.0.0
