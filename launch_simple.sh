#!/bin/bash

# Script simple pour lancer ParcInfo en mode HTTP
echo "🚀 LANCEMENT SIMPLE DE PARCINFO"
echo "================================"

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement rag_env..."
source rag_env/bin/activate

# Désactiver la redirection HTTPS
export SECURE_SSL_REDIRECT=False
export DEBUG=True

echo "🌐 Lancement en mode HTTP..."
echo "💡 URL : http://127.0.0.1:8000/"
echo "💡 Appuyez sur Ctrl+C pour arrêter"
echo ""

python manage.py runserver 127.0.0.1:8000
