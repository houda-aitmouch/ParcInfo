#!/bin/bash

# Script d'Installation et d'Utilisation des Diagrammes de Cas d'Utilisation - ParcInfo
# Auteur : Assistant IA
# Date : 2025

set -e  # Arrêt en cas d'erreur

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Fonction d'affichage avec couleurs
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo -e "${PURPLE}🏢 $1${NC}"
    echo "=================================================="
}

print_step() {
    echo -e "${CYAN}📋 $1${NC}"
}

# Vérification du système d'exploitation
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        OS="windows"
    else
        OS="unknown"
    fi
    echo "Système détecté : $OS"
}

# Installation de Java
install_java() {
    print_step "Vérification de Java..."
    
    if command -v java &> /dev/null; then
        JAVA_VERSION=$(java -version 2>&1 | head -n 1 | cut -d'"' -f2)
        print_success "Java est déjà installé : $JAVA_VERSION"
        return 0
    fi
    
    print_warning "Java n'est pas installé. Installation en cours..."
    
    case $OS in
        "linux")
            if command -v apt-get &> /dev/null; then
                sudo apt-get update
                sudo apt-get install -y openjdk-11-jdk
            elif command -v yum &> /dev/null; then
                sudo yum install -y java-11-openjdk-devel
            else
                print_error "Gestionnaire de paquets non reconnu. Installez Java manuellement."
                return 1
            fi
            ;;
        "macos")
            if command -v brew &> /dev/null; then
                brew install openjdk@11
                sudo ln -sfn /opt/homebrew/opt/openjdk@11/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-11.jdk
            else
                print_error "Homebrew n'est pas installé. Installez Java manuellement."
                return 1
            fi
            ;;
        "windows")
            print_error "Installez Java manuellement depuis https://adoptium.net/"
            return 1
            ;;
        *)
            print_error "Système d'exploitation non supporté"
            return 1
            ;;
    esac
    
    if command -v java &> /dev/null; then
        print_success "Java installé avec succès"
        return 0
    else
        print_error "Échec de l'installation de Java"
        return 1
    fi
}

# Installation de PlantUML
install_plantuml() {
    print_step "Vérification de PlantUML..."
    
    if command -v plantuml &> /dev/null; then
        PLANTUML_VERSION=$(plantuml -version 2>&1 | head -n 1)
        print_success "PlantUML est déjà installé : $PLANTUML_VERSION"
        return 0
    fi
    
    print_warning "PlantUML n'est pas installé. Installation en cours..."
    
    case $OS in
        "linux")
            if command -v apt-get &> /dev/null; then
                sudo apt-get install -y plantuml
            elif command -v yum &> /dev/null; then
                sudo yum install -y plantuml
            else
                print_warning "Installation manuelle de PlantUML..."
                install_plantuml_manual
            fi
            ;;
        "macos")
            if command -v brew &> /dev/null; then
                brew install plantuml
            else
                print_warning "Installation manuelle de PlantUML..."
                install_plantuml_manual
            fi
            ;;
        "windows")
            print_warning "Installation manuelle de PlantUML..."
            install_plantuml_manual
            ;;
        *)
            print_error "Système d'exploitation non supporté"
            return 1
            ;;
    esac
    
    if command -v plantuml &> /dev/null; then
        print_success "PlantUML installé avec succès"
        return 0
    else
        print_error "Échec de l'installation de PlantUML"
        return 1
    fi
}

# Installation manuelle de PlantUML
install_plantuml_manual() {
    print_step "Installation manuelle de PlantUML..."
    
    # Créer le répertoire bin s'il n'existe pas
    mkdir -p ~/bin
    
    # Télécharger PlantUML
    if [ ! -f ~/bin/plantuml.jar ]; then
        print_info "Téléchargement de PlantUML..."
        curl -L -o ~/bin/plantuml.jar https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar
    fi
    
    # Créer le script d'exécution
    cat > ~/bin/plantuml << 'EOF'
#!/bin/bash
java -jar ~/bin/plantuml.jar "$@"
EOF
    
    chmod +x ~/bin/plantuml
    
    # Ajouter au PATH si nécessaire
    if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
        echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
        echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
        export PATH="$HOME/bin:$PATH"
        print_info "PATH mis à jour. Redémarrez votre terminal ou exécutez 'source ~/.bashrc'"
    fi
}

# Vérification des prérequis
check_prerequisites() {
    print_header "Vérification des prérequis"
    
    detect_os
    
    # Vérification de Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1)
        print_success "Python3 est installé : $PYTHON_VERSION"
    else
        print_error "Python3 n'est pas installé"
        return 1
    fi
    
    # Installation de Java
    if ! install_java; then
        return 1
    fi
    
    # Installation de PlantUML
    if ! install_plantuml; then
        return 1
    fi
    
    print_success "Tous les prérequis sont satisfaits !"
    return 0
}

# Génération des diagrammes
generate_diagrams() {
    print_header "Génération des diagrammes"
    
    if [ ! -f "generate_diagrams.py" ]; then
        print_error "Script generate_diagrams.py non trouvé"
        return 1
    fi
    
    print_step "Exécution du script de génération..."
    python3 generate_diagrams.py
    
    if [ $? -eq 0 ]; then
        print_success "Diagrammes générés avec succès !"
        
        # Ouvrir le répertoire des diagrammes
        if [ -d "diagrammes_generes" ]; then
            print_info "Ouverture du répertoire des diagrammes..."
            case $OS in
                "linux")
                    xdg-open diagrammes_generes
                    ;;
                "macos")
                    open diagrammes_generes
                    ;;
                "windows")
                    start diagrammes_generes
                    ;;
            esac
        fi
    else
        print_error "Échec de la génération des diagrammes"
        return 1
    fi
}

# Affichage de l'aide
show_help() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  -h, --help     Affiche cette aide"
    echo "  -i, --install  Installe les prérequis uniquement"
    echo "  -g, --generate Génère les diagrammes uniquement"
    echo "  -a, --all      Installe les prérequis et génère les diagrammes (défaut)"
    echo ""
    echo "Exemples:"
    echo "  $0              # Installation complète + génération"
    echo "  $0 --install    # Installation des prérequis uniquement"
    echo "  $0 --generate   # Génération des diagrammes uniquement"
}

# Fonction principale
main() {
    print_header "ParcInfo - Gestion de Parc Informatique"
    print_info "Script d'installation et de génération des diagrammes de cas d'utilisation"
    echo ""
    
    # Traitement des arguments
    case "${1:-}" in
        -h|--help)
            show_help
            exit 0
            ;;
        -i|--install)
            if check_prerequisites; then
                print_success "Installation terminée avec succès !"
                print_info "Vous pouvez maintenant exécuter : $0 --generate"
            else
                print_error "Installation échouée"
                exit 1
            fi
            ;;
        -g|--generate)
            generate_diagrams
            ;;
        -a|--all|"")
            if check_prerequisites; then
                generate_diagrams
            else
                print_error "Installation des prérequis échouée"
                exit 1
            fi
            ;;
        *)
            print_error "Option invalide : $1"
            show_help
            exit 1
            ;;
    esac
}

# Exécution du script principal
main "$@"
