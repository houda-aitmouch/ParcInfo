#!/bin/bash

echo "🚀 Lancement du Dashboard Garantie ParcInfo"
echo "============================================="

# Vérifier si l'environnement virtuel existe
if [ ! -d "env" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv env
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source env/bin/activate

# Installer les dépendances
echo "📥 Installation des dépendances..."
pip install -r requirements.txt

# Lancer le dashboard
echo "🌐 Lancement du dashboard..."
echo "📍 Le dashboard sera accessible à l'adresse: http://localhost:8501"
echo "🔄 Appuyez sur Ctrl+C pour arrêter le dashboard"
echo ""

# Aller dans le dossier dashboard_garantie et lancer le dashboard
cd dashboard_garantie
streamlit run dashboard_garantie.py --server.port 8501 --server.address 0.0.0.0
