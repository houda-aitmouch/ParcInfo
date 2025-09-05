#!/bin/bash

echo "🚀 Démarrage de ParcInfo avec correction des fichiers statiques..."

# Activation de l'environnement virtuel
source rag_env/bin/activate

echo "📁 Vérification de la structure des fichiers statiques..."

# Création du dossier staticfiles s'il n'existe pas
if [ ! -d "staticfiles" ]; then
    echo "📁 Création du dossier staticfiles..."
    mkdir -p staticfiles
fi

# Vérification que les fichiers statiques existent
if [ ! -d "static" ]; then
    echo "❌ Erreur: Le dossier 'static' n'existe pas!"
    exit 1
fi

echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo "🔧 Vérification des permissions..."
chmod -R 755 staticfiles/
chmod -R 755 static/

echo "🌐 Démarrage du serveur Django..."
echo "📍 URL: http://127.0.0.1:9000"
echo "📁 Fichiers statiques: http://127.0.0.1:9000/static/"
echo ""
echo "💡 Pour tester les fichiers statiques:"
echo "   - CSS: http://127.0.0.1:9000/static/css/login.css"
echo "   - JS: http://127.0.0.1:9000/static/js/login.js"
echo "   - Images: http://127.0.0.1:9000/static/images/ADD.png"
echo ""
echo "⏹️  Arrêter avec Ctrl+C"
echo ""

# Démarrage du serveur
python manage.py runserver 127.0.0.1:9000
