#!/bin/bash

# Script pour lancer Django avec HTTPS en développement
# ParcInfo - Serveur HTTPS avec Uvicorn

echo "🚀 LANCEMENT DE PARCINFO EN HTTPS (UVICORN)"
echo "============================================="
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

# Vérifier que uvicorn est installé
echo "🧪 Vérification de uvicorn..."
python -c "import uvicorn; print('✅ uvicorn disponible')" || {
    echo "❌ uvicorn non disponible, installation..."
    pip install uvicorn
}

# Vérifier que les certificats existent
echo "🔍 Vérification des certificats SSL..."
if [ ! -f "cert.pem" ] || [ ! -f "key.pem" ]; then
    echo "❌ Certificats SSL manquants, création..."
    openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/C=MA/ST=Morocco/L=Casablanca/O=ParcInfo/CN=localhost"
fi

# Vérifier la configuration Django
echo "🔍 Vérification de la configuration Django..."
python manage.py check || {
    echo "❌ Problèmes de configuration Django détectés"
    exit 1
}

echo ""
echo "🎉 DJANGO OPÉRATIONNEL EN HTTPS AVEC UVICORN !"
echo ""

# Lancer Django avec HTTPS via uvicorn sur le port 8443
echo "🚀 Lancement de Django en HTTPS..."
echo "💡 Le serveur sera accessible sur https://127.0.0.1:8443/"
echo "💡 Acceptez le certificat auto-signé dans votre navigateur"
echo "💡 Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

uvicorn ParcInfo.asgi:application --host 127.0.0.1 --port 8443 --ssl-keyfile key.pem --ssl-certfile cert.pem --reload
