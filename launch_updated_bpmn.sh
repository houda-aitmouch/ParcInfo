#!/bin/bash
# Script de lancement pour la génération du diagramme BPMN ParcInfo mis à jour
# Auteur: Équipe ParcInfo
# Date: 2025-01-15

echo "🚀 Lancement de la génération du diagramme BPMN ParcInfo mis à jour..."
echo "=================================================================="

# Vérifier si nous sommes dans le bon répertoire
if [ ! -f "generate_updated_bpmn_diagram.py" ]; then
    echo "❌ Erreur: Ce script doit être exécuté depuis le répertoire ParcInfo"
    echo "💡 Utilisez: cd ParcInfo && ./launch_updated_bpmn.sh"
    exit 1
fi

# Vérifier si Python est disponible
if ! command -v python3 &> /dev/null; then
    echo "❌ Erreur: Python3 n'est pas installé ou n'est pas dans le PATH"
    echo "💡 Installez Python3 et réessayez"
    exit 1
fi

# Vérifier si l'environnement virtuel existe
if [ -d ".venv" ]; then
    echo "🔧 Activation de l'environnement virtuel..."
    source .venv/bin/activate
elif [ -d "venv" ]; then
    echo "🔧 Activation de l'environnement virtuel..."
    source venv/bin/activate
fi

# Vérifier si les dépendances sont installées
echo "📦 Vérification des dépendances..."
if ! python3 -c "import graphviz" 2>/dev/null; then
    echo "⚠️  Graphviz Python n'est pas installé. Installation en cours..."
    pip install graphviz
fi

# Vérifier si Graphviz système est installé
if ! command -v dot &> /dev/null; then
    echo "⚠️  Graphviz système n'est pas installé."
    echo "💻 Installation de Graphviz système..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            echo "🍺 Installation via Homebrew..."
            brew install graphviz
        else
            echo "❌ Homebrew n'est pas installé. Installez-le d'abord:"
            echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            echo "📦 Installation via apt-get..."
            sudo apt-get update && sudo apt-get install -y graphviz
        elif command -v yum &> /dev/null; then
            echo "📦 Installation via yum..."
            sudo yum install -y graphviz
        else
            echo "❌ Gestionnaire de paquets non reconnu. Installez Graphviz manuellement."
            exit 1
        fi
    else
        echo "❌ Système d'exploitation non supporté. Installez Graphviz manuellement depuis:"
        echo "   https://graphviz.org/download/"
        exit 1
    fi
fi

echo "✅ Toutes les dépendances sont installées!"

# Créer le répertoire de sortie s'il n'existe pas
mkdir -p diagrammes_generes

# Lancer la génération
echo "🔄 Génération du diagramme BPMN mis à jour..."
python3 generate_updated_bpmn_diagram.py

# Vérifier le succès
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Génération terminée avec succès!"
    echo "📁 Fichiers générés dans: diagrammes_generes/"
    
    # Lister les fichiers générés
    echo "📋 Fichiers créés:"
    ls -la diagrammes_generes/*.png 2>/dev/null | while read file; do
        echo "   - $(basename "$file")"
    done
    
    # Ouvrir le répertoire des diagrammes
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open diagrammes_generes/
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open diagrammes_generes/
    fi
    
else
    echo "❌ Erreur lors de la génération. Vérifiez les logs ci-dessus."
    exit 1
fi

echo ""
echo "🔍 NOUVELLES ÉTAPES AJOUTÉES AU DIAGRAMME:"
echo "   ✅ Archivage de la décharge après signature"
echo "   ✅ Gestion des commandes (papier/fichier)"
echo "   ✅ Suivi des livraisons avec dates et états"
echo "   ✅ Gestion du matériel et affectation"
echo "   ✅ Suivi des garanties et expiration"
echo ""
echo "📊 Le diagramme BPMN est maintenant complet avec toutes les étapes!"
