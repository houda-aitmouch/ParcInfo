#!/bin/bash

# Script pour lancer Django avec support HTTPS via proxy
# ParcInfo - Serveur Django avec configuration HTTPS

echo "🚀 LANCEMENT DE PARCINFO AVEC SUPPORT HTTPS"
echo "============================================="
echo "✅ Environnement : rag_env"
echo "✅ Serveur : Port 8000 (Django par défaut)"
echo "✅ Configuration : Support HTTPS via proxy"
echo ""

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement rag_env..."
source rag_env/bin/activate

# Vérifier que Python est disponible
echo "🧪 Vérification de Python..."
python --version || {
    echo "❌ Python non disponible dans l'environnement rag_env"
    exit 1
}

# Vérifier que Django est disponible
echo "🧪 Vérification de Django..."
python -c "import django; print(f'✅ Django {django.get_version()} disponible')" || {
    echo "❌ Django non disponible dans l'environnement rag_env"
    exit 1
}

# Vérifier la configuration Django
echo "🔍 Vérification de la configuration Django..."
python manage.py check || {
    echo "❌ Problèmes de configuration Django détectés"
    exit 1
}

echo ""
echo "🎉 DJANGO OPÉRATIONNEL AVEC SUPPORT HTTPS !"
echo ""

# Lancer Django avec configuration HTTPS
echo "🚀 Lancement de Django..."
echo "💡 Le serveur sera accessible sur :"
echo "   - HTTP : http://127.0.0.1:8000/"
echo "   - HTTPS : https://127.0.0.1:8000/ (via proxy)"
echo "💡 Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

# Configuration temporaire pour supporter HTTPS
export DJANGO_SETTINGS_MODULE=ParcInfo.settings
export SECURE_PROXY_SSL_HEADER="('HTTP_X_FORWARDED_PROTO', 'https')"
export SECURE_SSL_REDIRECT=False

python manage.py runserver 127.0.0.1:8000
