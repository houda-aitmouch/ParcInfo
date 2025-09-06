#!/bin/bash

echo "🧪 Test des services Docker ParcInfo"
echo "===================================="

# Fonction pour tester un endpoint
test_endpoint() {
    local url=$1
    local service_name=$2
    local expected_status=$3
    
    echo "🔍 Test de $service_name sur $url..."
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url" --max-time 10)
    
    if [ "$response" = "$expected_status" ]; then
        echo "✅ $service_name: OK (HTTP $response)"
    else
        echo "❌ $service_name: ÉCHEC (HTTP $response, attendu $expected_status)"
    fi
}

# Attendre un peu que les services démarrent
echo "⏳ Attente du démarrage des services..."
sleep 10

# Test des services
echo ""
echo "📊 Tests des services:"
echo "----------------------"

# Test du backend Django
test_endpoint "http://localhost:8000" "Backend Django" "200"

# Test du frontend React
test_endpoint "http://localhost:3000" "Frontend React" "200"

# Test du chatbot
test_endpoint "http://localhost:8001" "Chatbot" "200"

# Test de Streamlit
test_endpoint "http://localhost:8501" "Streamlit Dashboard" "200"

# Test de Nginx
test_endpoint "http://localhost:80" "Nginx Proxy" "200"

# Test de la base de données
echo ""
echo "🗄️ Test de la base de données:"
echo "------------------------------"

# Vérifier que le conteneur de la base de données est en cours d'exécution
if docker-compose ps | grep -q "db.*Up"; then
    echo "✅ Base de données PostgreSQL: Conteneur en cours d'exécution"
else
    echo "❌ Base de données PostgreSQL: Conteneur non démarré"
fi

# Test de connexion à la base de données
echo "🔍 Test de connexion à la base de données..."
if docker-compose exec -T db pg_isready -U Houda -d parcinfo_db; then
    echo "✅ Base de données PostgreSQL: Connexion OK"
else
    echo "❌ Base de données PostgreSQL: Connexion échouée"
fi

# Afficher les logs des services en cas d'erreur
echo ""
echo "📝 Logs des services (dernières 20 lignes):"
echo "--------------------------------------------"
docker-compose logs --tail=20

echo ""
echo "🏁 Tests terminés !"
