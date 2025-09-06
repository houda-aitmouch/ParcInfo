#!/bin/bash

echo "🚀 Démarrage des services ParcInfo via Kubernetes"
echo "=================================================="

# Vérifier que kubectl est disponible
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl n'est pas installé"
    exit 1
fi

# Vérifier que le namespace existe
if ! kubectl get namespace parcinfo &> /dev/null; then
    echo "❌ Le namespace 'parcinfo' n'existe pas"
    exit 1
fi

echo "✅ Namespace 'parcinfo' trouvé"

# Arrêter les port-forwards existants
echo "🔄 Arrêt des port-forwards existants..."
pkill -f "kubectl port-forward.*parcinfo" 2>/dev/null || true

# Attendre un peu
sleep 2

echo "🌐 Démarrage des port-forwards..."

# Backend Django
echo "📡 Backend Django sur http://localhost:8000"
kubectl port-forward -n parcinfo service/backend-service 8000:8000 &
BACKEND_PID=$!

# Chatbot
echo "🤖 Chatbot sur http://localhost:8001"
kubectl port-forward -n parcinfo service/chatbot-service 8001:8001 &
CHATBOT_PID=$!

# Streamlit Dashboard
echo "📊 Dashboard Streamlit sur http://localhost:8501"
kubectl port-forward -n parcinfo service/streamlit-service 8501:8501 &
STREAMLIT_PID=$!

# Frontend React
echo "⚛️  Frontend React sur http://localhost:3000"
kubectl port-forward -n parcinfo service/frontend-service 3000:3000 &
FRONTEND_PID=$!

# Attendre que les port-forwards se stabilisent
sleep 3

echo ""
echo "🎉 Services démarrés avec succès !"
echo ""
echo "📋 URLs d'accès :"
echo "   • Backend Django    : http://localhost:8000"
echo "   • Chatbot          : http://localhost:8001"
echo "   • Dashboard        : http://localhost:8501"
echo "   • Frontend React   : http://localhost:3000"
echo ""
echo "🔐 Pour accéder au chatbot, connectez-vous avec :"
echo "   • Utilisateur : admin"
echo "   • Email : admin@parcinfo.com"
echo "   • Ou créez un superutilisateur avec :"
echo "     kubectl exec -n parcinfo deployment/chatbot -- python manage.py createsuperuser"
echo ""
echo "⏹️  Pour arrêter tous les services :"
echo "   pkill -f 'kubectl port-forward.*parcinfo'"
echo ""

# Garder le script en vie
echo "🔄 Services en cours d'exécution... (Ctrl+C pour arrêter)"
wait
