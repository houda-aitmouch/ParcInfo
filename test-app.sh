#!/bin/bash

# Fonction pour afficher les messages d'information
print_info() {
    echo -e "\nℹ️  $1"
}

# Fonction pour afficher les messages de succès
print_success() {
    echo -e "✅ $1"
}

# Fonction pour afficher les messages d'erreur
print_error() {
    echo -e "❌ $1"
}

echo -e "\n🚀 Test de l'Application ParcInfo"
echo "================================="

# Test 1: Vérification des services Docker
print_info "Test 1: Vérification des services Docker..."
if docker-compose ps | grep -q "Up"; then
    print_success "Tous les services Docker sont en cours d'exécution"
else
    print_error "Certains services Docker ne sont pas démarrés"
    exit 1
fi

# Test 2: Test de l'accès principal
print_info "Test 2: Test de l'accès principal..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:80 | grep -q "302"; then
    print_success "Application accessible sur http://localhost:80 (redirection vers login)"
else
    print_error "Application inaccessible sur http://localhost:80"
    exit 1
fi

# Test 3: Test de la page de login
print_info "Test 3: Test de la page de login..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:80/accounts/login/ | grep -q "200"; then
    print_success "Page de login accessible"
else
    print_error "Page de login inaccessible"
    exit 1
fi

# Test 4: Test du backend direct
print_info "Test 4: Test du backend direct..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000 | grep -q "302"; then
    print_success "Backend accessible directement"
else
    print_error "Backend inaccessible directement"
    exit 1
fi

# Test 5: Test du frontend
print_info "Test 5: Test du frontend..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/health | grep -q "200"; then
    print_success "Frontend accessible"
else
    print_error "Frontend inaccessible"
    exit 1
fi

# Test 6: Test du chatbot
print_info "Test 6: Test du chatbot..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8001 | grep -q "200\|302"; then
    print_success "Chatbot accessible"
else
    print_error "Chatbot inaccessible"
    exit 1
fi

# Test 7: Test de Streamlit
print_info "Test 7: Test de Streamlit..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8501 | grep -q "200"; then
    print_success "Streamlit accessible directement"
else
    print_error "Streamlit inaccessible directement"
    exit 1
fi

# Test 8: Test de Streamlit via Nginx
print_info "Test 8: Test de Streamlit via Nginx..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:80/streamlit/ | grep -q "200"; then
    print_success "Streamlit accessible via Nginx"
else
    print_error "Streamlit inaccessible via Nginx"
    exit 1
fi

echo -e "\n✅ Tous les tests sont passés avec succès !"
echo -e "\n🌐 URLs d'accès :"
echo "  🏠 Application principale : http://localhost:80"
echo "  🔐 Page de login : http://localhost:80/accounts/login/"
echo "  🤖 Chatbot : http://localhost:80/chatbot/"
echo "  📊 Dashboard Streamlit : http://localhost:80/streamlit/"
echo "  🔧 Backend API : http://localhost:8000"
echo "  🎨 Frontend React : http://localhost:3000"

echo -e "\n🚀 L'application ParcInfo est prête à être utilisée !"
