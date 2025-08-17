#!/bin/bash

echo "📦 Installation des dépendances du Dashboard Garantie"
echo "=================================================="

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

echo "✅ Python3 détecté: $(python3 --version)"

# Créer l'environnement virtuel s'il n'existe pas
if [ ! -d "env" ]; then
    echo "🔧 Création de l'environnement virtuel..."
    python3 -m venv env
    echo "✅ Environnement virtuel créé"
else
    echo "✅ Environnement virtuel existant détecté"
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source env/bin/activate

# Mettre à jour pip
echo "📥 Mise à jour de pip..."
pip install --upgrade pip

# Installer les dépendances
echo "📥 Installation des dépendances..."
pip install -r requirements.txt

echo ""
echo "🎉 Installation terminée avec succès!"
echo ""
echo "📋 Prochaines étapes:"
echo "1. Testez la configuration: python dashboard_garantie/scripts/test_dashboard.py"
echo "2. Lancez le dashboard: ./dashboard_garantie/scripts/launch_dashboard.sh"
echo ""
echo "💡 Si vous rencontrez des erreurs, consultez le README_DASHBOARD.md"
