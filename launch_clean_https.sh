#!/bin/bash

echo "=== ParcInfo - Lancement Serveur HTTPS Propre ==="
echo ""

# Activer l'environnement virtuel
echo "1. Activation de l'environnement virtuel..."
source rag_env/bin/activate

# Nettoyer tous les processus Django existants
echo "2. Nettoyage des processus Django existants..."
pkill -f "python manage.py runserver" 2>/dev/null
pkill -f "python manage.py runserver_plus" 2>/dev/null
pkill -f "uvicorn" 2>/dev/null

# Attendre que les processus se terminent
sleep 3

# Vérifier qu'aucun processus ne tourne
echo "3. Vérification qu'aucun processus Django ne tourne..."
if pgrep -f "python manage.py" > /dev/null; then
    echo "   ⚠️  Des processus Django sont encore actifs. Arrêt forcé..."
    pkill -9 -f "python manage.py" 2>/dev/null
    sleep 2
else
    echo "   ✅ Aucun processus Django actif"
fi

# Vérifier les dépendances
echo "4. Vérification des dépendances..."
if ! python -c "import django_extensions" 2>/dev/null; then
    echo "   ⚠️  django-extensions non installé. Installation..."
    pip install django-extensions
fi

if ! python -c "import werkzeug" 2>/dev/null; then
    echo "   ⚠️  Werkzeug non installé. Installation..."
    pip install Werkzeug
fi

# Créer le répertoire SSL s'il n'existe pas
echo "5. Configuration des certificats SSL..."
mkdir -p ssl_certs

# Générer les certificats SSL s'ils n'existent pas
if [ ! -f ssl_certs/localhost.crt ] || [ ! -f ssl_certs/localhost.key ]; then
    echo "   🔐 Génération des certificats SSL auto-signés..."
    openssl req -x509 -newkey rsa:4096 -keyout ssl_certs/localhost.key -out ssl_certs/localhost.crt -days 365 -nodes -subj "/C=FR/ST=State/L=City/O=ParcInfo/CN=localhost" 2>/dev/null
    echo "   ✅ Certificats SSL générés"
else
    echo "   ✅ Certificats SSL existants trouvés"
fi

# Vérifier la base de données
echo "6. Vérification de la base de données..."
python manage.py check --database default

# Lancer le serveur HTTPS
echo ""
echo "7. Lancement du serveur Django en HTTPS..."
echo "   🔒 URL d'accès: https://127.0.0.1:8000/"
echo "   ⚠️  Note: Certificat auto-signé - acceptez l'avertissement dans votre navigateur"
echo "   📝 Logs: Regardez la console pour les messages"
echo "   ⏹️  Arrêt: Ctrl+C"
echo ""
echo "=== Démarrage du serveur HTTPS ==="
echo ""

python manage.py runserver_plus --cert-file ssl_certs/localhost.crt --key-file ssl_certs/localhost.key 127.0.0.1:8000
