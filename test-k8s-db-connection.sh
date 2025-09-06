#!/bin/bash

echo "🔧 Test de la configuration Kubernetes pour la base de données PostgreSQL locale"
echo "=================================================================================="

# Vérifier que kubectl est disponible
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl n'est pas installé ou n'est pas dans le PATH"
    exit 1
fi

# Vérifier que le cluster Kubernetes est accessible
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Impossible de se connecter au cluster Kubernetes"
    echo "   Assurez-vous que votre cluster est démarré (ex: minikube start)"
    exit 1
fi

echo "✅ Cluster Kubernetes accessible"

# Appliquer la configuration
echo "📦 Application de la configuration Kubernetes..."
kubectl apply -k k8s/

# Attendre que les pods soient prêts
echo "⏳ Attente du démarrage des pods..."
kubectl wait --for=condition=ready pod -l app=backend -n parcinfo --timeout=120s

if [ $? -eq 0 ]; then
    echo "✅ Pods backend prêts"
else
    echo "❌ Timeout lors du démarrage des pods backend"
    exit 1
fi

# Tester la connexion à la base de données
echo "🔍 Test de la connexion à la base de données..."
BACKEND_POD=$(kubectl get pods -n parcinfo -l app=backend -o jsonpath='{.items[0].metadata.name}')

if [ -z "$BACKEND_POD" ]; then
    echo "❌ Aucun pod backend trouvé"
    exit 1
fi

echo "📊 Pod backend trouvé: $BACKEND_POD"

# Tester la connexion à la base de données
echo "🔗 Test de la connexion à PostgreSQL..."
kubectl exec -n parcinfo $BACKEND_POD -- python manage.py shell -c "
from django.db import connection
cursor = connection.cursor()
cursor.execute('SELECT COUNT(*) FROM users_customuser')
print('✅ Utilisateurs dans la DB:', cursor.fetchone()[0])
cursor.execute('SELECT COUNT(*) FROM fournisseurs_fournisseur')
print('✅ Fournisseurs dans la DB:', cursor.fetchone()[0])
print('✅ Connexion à la base de données réussie!')
"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Configuration Kubernetes corrigée avec succès!"
    echo "   - Base de données: localhost:5432 (PostgreSQL local)"
    echo "   - Nom de la DB: parcinfo_db"
    echo "   - Utilisateur: Houda"
    echo ""
    echo "📋 Services disponibles:"
    kubectl get services -n parcinfo
    echo ""
    echo "📋 Pods en cours d'exécution:"
    kubectl get pods -n parcinfo
else
    echo "❌ Erreur lors du test de connexion à la base de données"
    echo "📋 Logs du pod backend:"
    kubectl logs -n parcinfo $BACKEND_POD --tail=20
    exit 1
fi
