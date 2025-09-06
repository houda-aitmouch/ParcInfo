#!/bin/bash

echo "🚀 Accès au Site ParcInfo - Déploiement Kubernetes"
echo "=================================================="

# Fonction pour afficher les messages
print_info() {
    echo -e "\nℹ️  $1"
}

print_success() {
    echo -e "✅ $1"
}

print_error() {
    echo -e "❌ $1"
}

# Vérifier l'état des pods
print_info "Vérification de l'état des services..."
kubectl get pods -n parcinfo

echo -e "\n"

# Configuration des port-forwards
print_info "Configuration des port-forwards..."

# Tuer les port-forwards existants
pkill -f "kubectl port-forward" 2>/dev/null || true

# Démarrer les port-forwards
print_info "Démarrage des port-forwards..."
kubectl port-forward -n parcinfo service/backend-service 8000:8000 &
kubectl port-forward -n parcinfo service/frontend-service 3000:3000 &
kubectl port-forward -n parcinfo service/streamlit-service 8501:8501 &
kubectl port-forward -n parcinfo service/chatbot-service 8001:8001 &

sleep 5

# Test des services
print_info "Test des services..."

echo -e "\n📱 ACCÈS AUX APPLICATIONS :"
echo "================================"

# Backend Django
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/ | grep -q "302\|200"; then
    print_success "Backend Django : http://localhost:8000"
    echo "   → Redirige vers /accounts/login/ (normal)"
else
    print_error "Backend Django : Non accessible"
fi

# Frontend React
if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/ | grep -q "301\|200"; then
    print_success "Frontend React : http://localhost:3000"
    echo "   → Interface utilisateur principale"
else
    print_error "Frontend React : Non accessible"
fi

# Dashboard Streamlit
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8501/ | grep -q "200"; then
    print_success "Dashboard Streamlit : http://localhost:8501"
    echo "   → Tableau de bord de gestion"
else
    print_error "Dashboard Streamlit : Non accessible"
fi

# Chatbot
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/ | grep -q "200\|404"; then
    print_success "Chatbot : http://localhost:8001"
    echo "   → Assistant IA (peut être en cours de démarrage)"
else
    print_error "Chatbot : Non accessible"
fi

echo -e "\n🎯 INSTRUCTIONS D'ACCÈS :"
echo "=========================="
echo "1. Ouvrez votre navigateur web"
echo "2. Accédez aux URLs ci-dessus"
echo "3. Pour l'interface principale : http://localhost:3000"
echo "4. Pour l'administration : http://localhost:8000/admin/"
echo "5. Pour le dashboard : http://localhost:8501"

echo -e "\n🔧 COMMANDES UTILES :"
echo "====================="
echo "• Voir les logs : kubectl logs -f deployment/backend -n parcinfo"
echo "• Redémarrer un service : kubectl rollout restart deployment/backend -n parcinfo"
echo "• Arrêter les port-forwards : pkill -f 'kubectl port-forward'"
echo "• Voir tous les services : kubectl get all -n parcinfo"

echo -e "\n✨ Le site ParcInfo est maintenant accessible via Kubernetes !"
