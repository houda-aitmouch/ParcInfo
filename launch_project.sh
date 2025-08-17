#!/bin/bash

# Script pour lancer Django et Streamlit simultanément
# ParcInfo - Dashboard de Garanties

echo "🚀 Lancement du projet ParcInfo..."
echo "📍 Port Django: 8000"
echo "📍 Port Streamlit: 8501"
echo ""

# Fonction pour arrêter tous les processus
cleanup() {
    echo ""
    echo "🛑 Arrêt des serveurs..."
    pkill -f "python manage.py runserver"
    pkill -f "streamlit run dashboard_garantie.py"
    echo "✅ Serveurs arrêtés"
    exit 0
}

# Capturer Ctrl+C pour arrêter proprement
trap cleanup SIGINT

# Vérifier si les ports sont disponibles
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo "❌ Port $port déjà utilisé"
        echo "   Arrêt des processus existants..."
        if [ $port -eq 8000 ]; then
            pkill -f "python manage.py runserver"
        elif [ $port -eq 8501 ]; then
            pkill -f "streamlit run dashboard_garantie.py"
        fi
        sleep 2
    fi
}

# Vérifier les ports
echo "🔍 Vérification des ports..."
check_port 8000
check_port 8501
echo "✅ Ports disponibles"
echo ""

# Lancer Django en arrière-plan
echo "🌐 Démarrage du serveur Django..."
cd /Users/HouDa/PycharmProjects/ParcInfo
python manage.py runserver 8000 &
DJANGO_PID=$!
echo "✅ Django démarré (PID: $DJANGO_PID)"
echo "   URL: http://localhost:8000"
echo ""

# Attendre un peu pour que Django démarre
sleep 3

# Lancer Streamlit en arrière-plan
echo "📊 Démarrage du serveur Streamlit..."
cd /Users/HouDa/PycharmProjects/ParcInfo/dashboard_garantie
python -m streamlit run dashboard_garantie.py --server.port 8501 --server.headless true &
STREAMLIT_PID=$!
echo "✅ Streamlit démarré (PID: $STREAMLIT_PID)"
echo "   URL: http://localhost:8501"
echo ""

# Attendre un peu pour que Streamlit démarre
sleep 5

# Vérifier que les serveurs fonctionnent
echo "🔍 Vérification des serveurs..."
if curl -s -I http://localhost:8000 > /dev/null 2>&1; then
    echo "✅ Django accessible sur http://localhost:8000"
else
    echo "❌ Django non accessible"
fi

if curl -s -I http://localhost:8501 > /dev/null 2>&1; then
    echo "✅ Streamlit accessible sur http://localhost:8501"
else
    echo "❌ Streamlit non accessible"
fi

echo ""
echo "🎉 Projet ParcInfo lancé avec succès !"
echo ""
echo "📋 URLs disponibles :"
echo "   🌐 Django: http://localhost:8000"
echo "   📊 Dashboard Garanties: http://localhost:8501"
echo ""
echo "💡 Pour arrêter les serveurs, appuyez sur Ctrl+C"
echo ""

# Attendre indéfiniment
while true; do
    sleep 1
done
