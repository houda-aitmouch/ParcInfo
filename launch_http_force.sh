#!/bin/bash

# Script pour forcer HTTP en contournant la détection automatique de HTTPS
# ParcInfo - Serveur HTTP forcé

echo "🚀 LANCEMENT DE PARCINFO EN HTTP FORCÉ"
echo "======================================="
echo "✅ Environnement : rag_env"
echo "✅ Serveur : Port 9000 (HTTP forcé)"
echo "✅ Mode : Contournement détection HTTPS"
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
echo "🎉 DJANGO OPÉRATIONNEL EN HTTP FORCÉ !"
echo ""

# Configuration pour forcer HTTP
export DJANGO_SETTINGS_MODULE=ParcInfo.settings
export SECURE_SSL_REDIRECT=False
export SECURE_PROXY_SSL_HEADER=""
export SECURE_HSTS_SECONDS=0
export SECURE_HSTS_INCLUDE_SUBDOMAINS=False
export SECURE_HSTS_PRELOAD=False
export SESSION_COOKIE_SECURE=False
export CSRF_COOKIE_SECURE=False
export DEBUG=True

# Variables pour contourner la détection HTTPS
export HTTP_X_FORWARDED_PROTO=http
export HTTP_X_FORWARDED_SSL=off
export HTTPS=off

# Lancer Django en HTTP forcé
echo "🚀 Lancement de Django en HTTP forcé..."
echo "💡 Le serveur sera accessible sur : http://127.0.0.1:9000/"
echo "💡 Variables d'environnement HTTP forcées"
echo "💡 Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

python manage.py runserver 127.0.0.1:9000
