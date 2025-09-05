#!/bin/bash

# Script final qui fonctionne - ParcInfo sans redirection HTTPS
# ParcInfo - Serveur HTTP fonctionnel

echo "🚀 LANCEMENT FINAL FONCTIONNEL DE PARCINFO"
echo "==========================================="
echo "✅ Environnement : rag_env"
echo "✅ Serveur : Port 9000 (HTTP simple)"
echo "✅ Mode : Sans redirection HTTPS"
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
echo "🎉 DJANGO OPÉRATIONNEL !"
echo ""

# Lancer Django sur le port 9000
echo "🚀 Lancement de Django sur le port 9000..."
echo "💡 Le serveur sera accessible sur : http://127.0.0.1:9000/"
echo "💡 Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

# Configuration pour HTTP simple
export DJANGO_SETTINGS_MODULE=ParcInfo.settings
export SECURE_SSL_REDIRECT=False
export SECURE_PROXY_SSL_HEADER=""
export DEBUG=True

# Lancer le serveur sur le port 9000
python manage.py runserver 127.0.0.1:9000
