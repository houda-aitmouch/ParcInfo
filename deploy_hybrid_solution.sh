#!/bin/bash

# Script de déploiement de la solution hybride Kubernetes + Docker
# ParcInfo - Backend/Frontend/Streamlit en Kubernetes + Chatbot en Docker

echo "🚀 Déploiement de la solution hybride ParcInfo"
echo "=============================================="

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "docker-compose.yml" ]; then
    print_error "Ce script doit être exécuté depuis le répertoire racine de ParcInfo"
    exit 1
fi

print_status "Début du déploiement de la solution hybride..."

# Étape 1: Nettoyer les déploiements existants
print_status "1️⃣ Nettoyage des déploiements existants..."
kubectl delete deployment chatbot -n parcinfo 2>/dev/null || true
docker-compose down 2>/dev/null || true
pkill -f "kubectl port-forward" 2>/dev/null || true

# Étape 2: Construire les images Docker
print_status "2️⃣ Construction des images Docker..."
docker build -f Dockerfile.backend -t parcinfo-backend:latest .
docker build -f Dockerfile.streamlit -t parcinfo-streamlit:latest .
docker build -f Dockerfile.chatbot -t parcinfo-chatbot:latest .

if [ $? -eq 0 ]; then
    print_success "Images Docker construites avec succès"
else
    print_error "Échec de la construction des images Docker"
    exit 1
fi

# Étape 3: Déployer les services Kubernetes
print_status "3️⃣ Déploiement des services Kubernetes..."
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/streamlit.yaml
kubectl apply -f k8s/frontend.yaml

if [ $? -eq 0 ]; then
    print_success "Services Kubernetes déployés avec succès"
else
    print_error "Échec du déploiement Kubernetes"
    exit 1
fi

# Étape 4: Démarrer le chatbot Docker
print_status "4️⃣ Démarrage du chatbot Docker..."
docker-compose up -d chatbot

if [ $? -eq 0 ]; then
    print_success "Chatbot Docker démarré avec succès"
else
    print_error "Échec du démarrage du chatbot Docker"
    exit 1
fi

# Étape 5: Attendre que tous les services soient prêts
print_status "5️⃣ Attente que tous les services soient prêts..."
echo "Attente des pods Kubernetes..."
kubectl wait --for=condition=ready pod -l app=backend -n parcinfo --timeout=300s
kubectl wait --for=condition=ready pod -l app=streamlit -n parcinfo --timeout=300s
kubectl wait --for=condition=ready pod -l app=frontend -n parcinfo --timeout=300s

echo "Attente du chatbot Docker..."
sleep 30

# Étape 6: Vérifier le statut des services
print_status "6️⃣ Vérification du statut des services..."

echo "Pods Kubernetes:"
kubectl get pods -n parcinfo

echo ""
echo "Services Kubernetes:"
kubectl get services -n parcinfo

echo ""
echo "Containers Docker:"
docker ps --filter "name=parcinfo"

# Étape 7: Tester les services
print_status "7️⃣ Test des services..."

# Test du backend
echo "Test du backend Kubernetes..."
kubectl port-forward -n parcinfo service/backend-service 8000:8000 &
BACKEND_PID=$!
sleep 5

if curl -s http://localhost:8000/ > /dev/null; then
    print_success "Backend Kubernetes accessible"
else
    print_warning "Backend Kubernetes non accessible"
fi

# Test de Streamlit
echo "Test de Streamlit Kubernetes..."
kubectl port-forward -n parcinfo service/streamlit-service 8501:8501 &
STREAMLIT_PID=$!
sleep 5

if curl -s http://localhost:8501/ > /dev/null; then
    print_success "Streamlit Kubernetes accessible"
else
    print_warning "Streamlit Kubernetes non accessible"
fi

# Test du chatbot Docker
echo "Test du chatbot Docker..."
sleep 10
if curl -s -X POST http://localhost:8001/chatbot/api/ -H "Content-Type: application/json" -d '{"query":"test"}' > /dev/null; then
    print_success "Chatbot Docker accessible"
else
    print_warning "Chatbot Docker non accessible"
fi

# Nettoyer les port-forwards de test
kill $BACKEND_PID $STREAMLIT_PID 2>/dev/null || true

# Étape 8: Afficher les URLs d'accès
print_status "8️⃣ URLs d'accès:"
echo ""
echo "🌐 URLs d'accès:"
echo "   - Backend Django: http://localhost:8000/"
echo "   - Dashboard Garantie: http://localhost:8000/dashboard-garantie/"
echo "   - Streamlit: http://localhost:8501/"
echo "   - Chatbot Web: http://localhost:8001/chatbot/"
echo "   - Chatbot API: http://localhost:8001/chatbot/api/"
echo ""
echo "🔧 Pour accéder aux services, utilisez:"
echo "   kubectl port-forward -n parcinfo service/backend-service 8000:8000 &"
echo "   kubectl port-forward -n parcinfo service/streamlit-service 8501:8501 &"
echo ""

print_success "Déploiement de la solution hybride terminé !"
print_status "Architecture: Kubernetes (Backend/Frontend/Streamlit) + Docker (Chatbot)"
