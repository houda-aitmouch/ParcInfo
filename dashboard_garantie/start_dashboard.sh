#!/bin/bash

# Script de démarrage automatique du Dashboard de Garanties
# Usage: ./start_dashboard.sh [port]

# Port par défaut
PORT=${1:-8501}

echo "🚀 Démarrage du Dashboard de Garanties ParcInfo..."
echo "📍 Port: $PORT"
echo "🌐 URL: http://localhost:$PORT"
echo ""

# Vérifier si le port est déjà utilisé
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Le port $PORT est déjà utilisé par un autre processus."
    echo "🔍 Processus utilisant le port $PORT :"
    lsof -Pi :$PORT -sTCP:LISTEN
    echo ""
    echo "🛑 Arrêt du processus existant..."
    pkill -f "streamlit run dashboard_garantie.py"
    sleep 2
fi

# Vérifier que le fichier Python existe
if [ ! -f "dashboard_garantie.py" ]; then
    echo "❌ Erreur: Le fichier dashboard_garantie.py n'existe pas dans le répertoire actuel"
    echo "📁 Répertoire actuel: $(pwd)"
    exit 1
fi

# Démarrer le serveur Streamlit
echo "▶️  Démarrage du serveur Streamlit..."
echo "⏳ Veuillez patienter quelques secondes..."
echo ""

python -m streamlit run dashboard_garantie.py --server.port $PORT --server.headless true

echo ""
echo "🛑 Serveur arrêté."
