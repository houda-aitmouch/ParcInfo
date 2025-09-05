#!/bin/bash

# Script de lancement pour la génération des diagrammes ParcInfo
# =============================================================

echo "🚀 Lancement de la génération des diagrammes ParcInfo..."
echo ""

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Erreur: Python3 n'est pas installé ou n'est pas dans le PATH"
    exit 1
fi

# Vérifier si pip est installé
if ! command -v pip3 &> /dev/null; then
    echo "❌ Erreur: pip3 n'est pas installé"
    exit 1
fi

# Vérifier si l'environnement virtuel existe
if [ ! -d "graphviz_env" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv graphviz_env
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source graphviz_env/bin/activate

# Installer les dépendances si nécessaire
echo "📦 Vérification des dépendances..."
if ! python -c "import graphviz" 2>/dev/null; then
    echo "📥 Installation de Graphviz Python..."
    pip install -r requirements_graphviz.txt
fi

# Vérifier si Graphviz système est installé
if ! command -v dot &> /dev/null; then
    echo "⚠️  Attention: Graphviz système n'est pas installé"
    echo "💻 Installation recommandée:"
    echo "   - macOS: brew install graphviz"
    echo "   - Ubuntu/Debian: sudo apt-get install graphviz"
    echo "   - CentOS/RHEL: sudo yum install graphviz"
    echo "   - Windows: télécharger depuis https://graphviz.org/"
    echo ""
    echo "🔄 Tentative de génération sans Graphviz système..."
fi

# Lancer la génération
echo "🎨 Génération des diagrammes..."
python generate_workflow_diagram.py

# Désactiver l'environnement virtuel
deactivate

echo ""
echo "✅ Script terminé!"
echo "📁 Les diagrammes ont été générés dans: diagrammes_generes/"
