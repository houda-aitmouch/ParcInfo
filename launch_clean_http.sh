#!/bin/bash

echo "=== ParcInfo - Lancement Serveur HTTP Propre ==="
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

# Vérifier la base de données
echo "5. Vérification de la base de données..."
python manage.py check --database default

# Lancer le serveur HTTP
echo ""
echo "6. Lancement du serveur Django en HTTP..."
echo "   🌐 URL d'accès: http://127.0.0.1:8000/"
echo "   📝 Logs: Regardez la console pour les messages"
echo "   ⏹️  Arrêt: Ctrl+C"
echo ""
echo "=== Démarrage du serveur ==="
echo ""

python manage.py runserver 127.0.0.1:8000
