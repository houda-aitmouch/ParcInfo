#!/bin/bash

# Script de nettoyage des diagrammes UML générés
# Usage: ./clean_uml_diagrams.sh

echo "🧹 Nettoyage des diagrammes UML générés..."

# Supprimer le dossier des diagrammes générés
if [ -d "diagrammes_generes" ]; then
    rm -rf diagrammes_generes
    echo "✅ Dossier 'diagrammes_generes' supprimé"
else
    echo "ℹ️  Dossier 'diagrammes_generes' n'existe pas"
fi

# Supprimer les fichiers PNG et SVG isolés (s'ils existent)
find . -maxdepth 1 -name "*.png" -delete
find . -maxdepth 1 -name "*.svg" -delete

echo "✅ Nettoyage terminé"
echo "💡 Pour régénérer les diagrammes, exécutez: python3 generate_uml_diagrams.py"
