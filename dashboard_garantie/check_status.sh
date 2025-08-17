#!/bin/bash

# Script de vérification de l'état du Dashboard de Garanties
# Usage: ./check_status.sh [port]

# Port par défaut
PORT=${1:-8501}

echo "🔍 Vérification de l'état du Dashboard de Garanties ParcInfo..."
echo "📍 Port: $PORT"
echo ""

# Vérifier si le processus Streamlit est en cours d'exécution
if pgrep -f "streamlit run dashboard_garantie.py" > /dev/null; then
    echo "✅ Processus Streamlit actif"
    echo "📊 Informations du processus :"
    ps aux | grep "streamlit run dashboard_garantie.py" | grep -v grep
    echo ""
else
    echo "❌ Aucun processus Streamlit trouvé"
    echo ""
fi

# Vérifier si le port est en écoute
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo "✅ Port $PORT en écoute"
    echo "🔍 Processus utilisant le port $PORT :"
    lsof -Pi :$PORT -sTCP:LISTEN
    echo ""
else
    echo "❌ Port $PORT non accessible"
    echo ""
fi

# Tester la connectivité HTTP
echo "🌐 Test de connectivité HTTP..."
if curl -s -I http://localhost:$PORT > /dev/null 2>&1; then
    echo "✅ Serveur HTTP accessible sur http://localhost:$PORT"
    
    # Récupérer le statut HTTP
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT)
    echo "📊 Statut HTTP: $HTTP_STATUS"
    
    # Récupérer le temps de réponse
    RESPONSE_TIME=$(curl -s -o /dev/null -w "%{time_total}" http://localhost:$PORT)
    echo "⏱️  Temps de réponse: ${RESPONSE_TIME}s"
    
else
    echo "❌ Serveur HTTP non accessible sur http://localhost:$PORT"
fi

echo ""
echo "📋 Résumé de l'état :"

# Évaluation globale
if pgrep -f "streamlit run dashboard_garantie.py" > /dev/null && lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null && curl -s -I http://localhost:$PORT > /dev/null 2>&1; then
    echo "🟢 Dashboard opérationnel"
    echo "   - Processus actif"
    echo "   - Port en écoute"
    echo "   - Serveur HTTP accessible"
    echo ""
    echo "🌐 Accès: http://localhost:$PORT"
elif pgrep -f "streamlit run dashboard_garantie.py" > /dev/null && lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null; then
    echo "🟡 Dashboard partiellement opérationnel"
    echo "   - Processus actif"
    echo "   - Port en écoute"
    echo "   - Serveur HTTP non accessible"
    echo ""
    echo "💡 Suggestion: Redémarrer le serveur"
elif pgrep -f "streamlit run dashboard_garantie.py" > /dev/null; then
    echo "🟡 Dashboard partiellement opérationnel"
    echo "   - Processus actif"
    echo "   - Port non en écoute"
    echo "   - Serveur HTTP non accessible"
    echo ""
    echo "💡 Suggestion: Vérifier la configuration du port"
else
    echo "🔴 Dashboard non opérationnel"
    echo "   - Aucun processus actif"
    echo "   - Port non en écoute"
    echo "   - Serveur HTTP non accessible"
    echo ""
    echo "💡 Suggestion: Démarrer le dashboard avec ./start_dashboard.sh"
fi

echo ""
echo "🔧 Actions recommandées :"
echo "   - Démarrer: ./start_dashboard.sh"
echo "   - Arrêter: pkill -f 'streamlit run dashboard_garantie.py'"
echo "   - Redémarrer: ./start_dashboard.sh"
echo "   - Vérifier les logs: tail -f ~/.streamlit/logs/streamlit.log"
