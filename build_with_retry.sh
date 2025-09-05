#!/bin/bash

# Script de build Docker avec retry logic pour résoudre les problèmes de timeout
# Usage: ./build_with_retry.sh [image_name] [max_attempts]

set -e

IMAGE_NAME=${1:-"parcinfo-web"}
MAX_ATTEMPTS=${2:-3}
BUILD_TIMEOUT=3600  # 1 heure

echo "🚀 Démarrage du build Docker avec retry logic..."
echo "📦 Image: $IMAGE_NAME"
echo "🔄 Tentatives max: $MAX_ATTEMPTS"
echo "⏱️  Timeout: ${BUILD_TIMEOUT}s"

# Fonction pour nettoyer les images Docker
cleanup_docker() {
    echo "🧹 Nettoyage des images Docker..."
    docker system prune -f || true
    docker builder prune -f || true
}

# Fonction pour vérifier la connectivité
check_connectivity() {
    echo "🌐 Vérification de la connectivité..."
    if curl -s --max-time 10 https://huggingface.co > /dev/null; then
        echo "✅ Connectivité Hugging Face OK"
        return 0
    else
        echo "❌ Problème de connectivité Hugging Face"
        return 1
    fi
}

# Fonction de build avec timeout (compatible macOS)
build_image() {
    local attempt=$1
    echo "🔨 Tentative de build $attempt/$MAX_ATTEMPTS..."
    
    # Utiliser gtimeout si disponible (installé via brew install coreutils)
    # Sinon, utiliser docker build normal
    if command -v gtimeout > /dev/null 2>&1; then
        echo "⏱️  Utilisation de gtimeout (${BUILD_TIMEOUT}s)"
        gtimeout $BUILD_TIMEOUT docker build \
            --no-cache \
            --build-arg BUILDKIT_INLINE_CACHE=1 \
            --progress=plain \
            -t "$IMAGE_NAME" . || {
            echo "⏰ Build timeout après ${BUILD_TIMEOUT}s"
            return 1
        }
    else
        echo "⚠️  gtimeout non disponible, build sans timeout"
        echo "💡 Pour installer: brew install coreutils"
        docker build \
            --no-cache \
            --build-arg BUILDKIT_INLINE_CACHE=1 \
            --progress=plain \
            -t "$IMAGE_NAME" .
    fi
}

# Fonction principale
main() {
    local attempt=1
    
    while [ $attempt -le $MAX_ATTEMPTS ]; do
        echo ""
        echo "🔄 === TENTATIVE $attempt/$MAX_ATTEMPTS ==="
        
        # Vérifier la connectivité
        if ! check_connectivity; then
            echo "⏳ Attente de 30 secondes avant de réessayer..."
            sleep 30
        fi
        
        # Nettoyer Docker si ce n'est pas la première tentative
        if [ $attempt -gt 1 ]; then
            cleanup_docker
        fi
        
        # Tentative de build
        if build_image $attempt; then
            echo "🎉 Build réussi!"
            echo "📊 Informations sur l'image:"
            docker images "$IMAGE_NAME" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
            exit 0
        else
            echo "❌ Build échoué (tentative $attempt/$MAX_ATTEMPTS)"
            
            if [ $attempt -lt $MAX_ATTEMPTS ]; then
                local wait_time=$((attempt * 30))  # Attente progressive: 30s, 60s, 90s
                echo "⏳ Attente de ${wait_time}s avant la prochaine tentative..."
                sleep $wait_time
            fi
        fi
        
        attempt=$((attempt + 1))
    done
    
    echo "💥 Toutes les tentatives ont échoué!"
    echo "🔍 Suggestions de dépannage:"
    echo "   - Vérifiez votre connexion internet"
    echo "   - Essayez de redémarrer Docker"
    echo "   - Vérifiez l'espace disque disponible"
    echo "   - Consultez les logs Docker: docker system events"
    
    exit 1
}

# Vérifier que Docker est en cours d'exécution
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker n'est pas en cours d'exécution!"
    exit 1
fi

# Exécuter le script principal
main "$@"
