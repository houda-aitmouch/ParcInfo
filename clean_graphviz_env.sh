#!/bin/bash

# Script de nettoyage pour l'environnement Graphviz
# ================================================

echo "🧹 Nettoyage de l'environnement Graphviz..."

# Vérifier si l'environnement virtuel existe
if [ -d "graphviz_env" ]; then
    echo "🗑️  Suppression de l'environnement virtuel graphviz_env..."
    rm -rf graphviz_env
    echo "✅ Environnement virtuel supprimé"
else
    echo "ℹ️  Aucun environnement virtuel à supprimer"
fi

# Vérifier s'il y a des fichiers temporaires à nettoyer
if [ -f "diagrammes_generes/workflow_parcinfo_complet" ]; then
    echo "🗑️  Suppression des fichiers temporaires..."
    rm -f diagrammes_generes/workflow_parcinfo_complet
    rm -f diagrammes_generes/roles_parcinfo
    echo "✅ Fichiers temporaires supprimés"
fi

echo ""
echo "✅ Nettoyage terminé!"
