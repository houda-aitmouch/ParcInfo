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

echo -e "\n🚀 Démarrage Kubernetes - ParcInfo"
echo "=================================="

# Vérification de Docker Desktop
print_info "Vérification de Docker Desktop..."
if ! docker info &> /dev/null; then
    print_error "Docker n'est pas démarré"
    print_info "Démarrage de Docker Desktop..."
    open -a "Docker Desktop"
    print_info "Attente du démarrage de Docker Desktop..."
    sleep 30
fi

# Vérification de kubectl
print_info "Vérification de kubectl..."
if ! command -v kubectl &> /dev/null; then
    print_error "kubectl n'est pas installé"
    exit 1
fi

# Attente de la disponibilité du cluster
print_info "Attente de la disponibilité du cluster Kubernetes..."
for i in {1..30}; do
    if kubectl cluster-info &> /dev/null; then
        print_success "Cluster Kubernetes disponible"
        break
    fi
    if [ $i -eq 30 ]; then
        print_error "Cluster Kubernetes non disponible après 5 minutes"
        print_info "Vérifiez que Kubernetes est activé dans Docker Desktop"
        exit 1
    fi
    print_info "Tentative $i/30 - Attente..."
    sleep 10
done

# Déploiement
print_info "Déploiement de l'application ParcInfo sur Kubernetes..."
if ./deploy-k8s.sh; then
    print_success "Déploiement Kubernetes réussi !"
else
    print_error "Erreur lors du déploiement Kubernetes"
    exit 1
fi

# Configuration du port-forward
print_info "Configuration du port-forward pour l'accès local..."
kubectl port-forward -n parcinfo service/nginx-service 8080:80 &
PORT_FORWARD_PID=$!

print_success "Port-forward configuré (PID: $PORT_FORWARD_PID)"
print_info "Application accessible sur : http://localhost:8080"

echo -e "\n🎯 Commandes utiles :"
echo "  - Voir les pods : kubectl get pods -n parcinfo"
echo "  - Voir les services : kubectl get services -n parcinfo"
echo "  - Voir les logs : kubectl logs -f deployment/backend -n parcinfo"
echo "  - Arrêter le port-forward : kill $PORT_FORWARD_PID"
echo "  - Supprimer l'application : kubectl delete namespace parcinfo"
