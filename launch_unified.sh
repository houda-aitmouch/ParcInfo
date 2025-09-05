#!/bin/bash

# Script unifié pour lancer ParcInfo
# ParcInfo - Choix entre HTTP et HTTPS

echo "🚀 LANCEMENT UNIFIÉ DE PARCINFO"
echo "================================"
echo "✅ Environnement : rag_env"
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

# Menu de choix
echo "📋 Choisissez votre mode de lancement :"
echo ""
echo "1️⃣  HTTP (Port 8000) - Rapide et simple"
echo "2️⃣  HTTPS (Port 8000) - Sécurisé avec certificat auto-signé"
echo "3️⃣  Quitter"
echo ""

read -p "Votre choix (1-3) : " choice

case $choice in
    1)
        echo ""
        echo "🌐 Lancement en mode HTTP..."
        echo "💡 URL : http://127.0.0.1:8000/"
        echo "💡 Appuyez sur Ctrl+C pour arrêter"
        echo ""
        python manage.py runserver 127.0.0.1:8000
        ;;
    2)
        echo ""
        echo "🔒 Lancement en mode HTTPS..."
        
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
        
        echo "💡 URL : https://127.0.0.1:8000/"
        echo "💡 Acceptez le certificat auto-signé dans votre navigateur"
        echo "💡 Appuyez sur Ctrl+C pour arrêter"
        echo ""
        uvicorn ParcInfo.asgi:application --host 127.0.0.1 --port 8000 --ssl-keyfile key.pem --ssl-certfile cert.pem --reload
        ;;
    3)
        echo ""
        echo "👋 Au revoir !"
        exit 0
        ;;
    *)
        echo ""
        echo "❌ Choix invalide. Veuillez choisir 1, 2 ou 3."
        exit 1
        ;;
esac
