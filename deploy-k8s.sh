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

echo -e "\n🚀 Déploiement Kubernetes - ParcInfo"
echo "====================================="

# Vérification de kubectl
print_info "Vérification de kubectl..."
if ! command -v kubectl &> /dev/null; then
    print_error "kubectl n'est pas installé"
    exit 1
fi
print_success "kubectl est installé"

# Vérification de la connexion au cluster
print_info "Vérification de la connexion au cluster Kubernetes..."
if kubectl cluster-info &> /dev/null; then
    print_success "Connexion au cluster Kubernetes établie"
else
    print_error "Impossible de se connecter au cluster Kubernetes"
    print_info "Assurez-vous que Docker Desktop est démarré avec Kubernetes activé"
    print_info "Ou utilisez: minikube start"
    exit 1
fi

# Vérification des manifests
print_info "Vérification des manifests Kubernetes..."
if [ ! -d "k8s" ]; then
    print_error "Le dossier k8s n'existe pas"
    exit 1
fi

# Test des manifests avec dry-run
print_info "Test des manifests avec dry-run..."
if kubectl apply -k k8s/ --dry-run=client &> /dev/null; then
    print_success "Manifests Kubernetes valides"
else
    print_error "Erreur dans les manifests Kubernetes"
    kubectl apply -k k8s/ --dry-run=client
    exit 1
fi

# Déploiement
print_info "Déploiement des ressources Kubernetes..."
if kubectl apply -k k8s/; then
    print_success "Ressources Kubernetes déployées avec succès"
else
    print_error "Erreur lors du déploiement"
    exit 1
fi

# Vérification du déploiement
print_info "Vérification du déploiement..."
kubectl get pods -n parcinfo
kubectl get services -n parcinfo
kubectl get ingress -n parcinfo

print_success "Déploiement Kubernetes terminé !"
print_info "Pour accéder à l'application :"
print_info "  - Port-forward : kubectl port-forward -n parcinfo service/nginx-service 8080:80"
print_info "  - Puis ouvrir : http://localhost:8080"
