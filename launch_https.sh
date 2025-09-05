#!/bin/bash

# Script pour lancer Django avec HTTPS en développement
# ParcInfo - Serveur HTTPS

echo "🚀 LANCEMENT DE PARCINFO EN HTTPS"
echo "=================================="
echo "✅ Environnement : rag_env"
echo "✅ Serveur HTTPS : Port 8443"
echo "✅ Certificat auto-signé (accepter l'avertissement)"
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

# Vérifier que sslserver est installé
echo "🧪 Vérification de sslserver..."
python -c "import sslserver; print('✅ sslserver disponible')" || {
    echo "❌ sslserver non disponible, installation..."
    pip install django-sslserver
}

# Vérifier la configuration Django
echo "🔍 Vérification de la configuration Django..."
python manage.py check || {
    echo "❌ Problèmes de configuration Django détectés"
    exit 1
}

echo ""
echo "🎉 DJANGO OPÉRATIONNEL EN HTTPS !"
echo ""

# Lancer Django avec HTTPS
echo "🚀 Lancement de Django en HTTPS..."
echo "💡 Le serveur sera accessible sur https://127.0.0.1:8443/"
echo "💡 Acceptez le certificat auto-signé dans votre navigateur"
echo "💡 Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

python manage.py runsslserver 127.0.0.1:8443
