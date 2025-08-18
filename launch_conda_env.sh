#!/bin/bash
# Script de lancement de ParcInfo avec l'environnement conda
# Utilise l'environnement conda ParcInfo pour Django

echo "🚀 LANCEMENT DE PARCINFO AVEC ENVIRONNEMENT CONDA"
echo "=================================================="
echo "✅ Environnement : conda ParcInfo"
echo "✅ Django 5.2.4 installé et fonctionnel"
echo "✅ Toutes les dépendances de base installées"
echo ""

# Activer l'environnement conda
echo "🔧 Activation de l'environnement conda ParcInfo..."
conda activate ParcInfo

# Vérifier que Python est disponible
echo "🧪 Vérification de Python..."
python --version || {
    echo "❌ Python non disponible dans l'environnement conda"
    exit 1
}

# Vérifier que Django est disponible
echo "🧪 Vérification de Django..."
python -c "import django; print(f'✅ Django {django.get_version()} disponible')" || {
    echo "❌ Django non disponible dans l'environnement conda"
    exit 1
}

# Vérifier la configuration Django
echo "🔍 Vérification de la configuration Django..."
python manage.py check || {
    echo "❌ Problèmes de configuration Django détectés"
    exit 1
}

echo ""
echo "🎉 DJANGO OPÉRATIONNEL DANS L'ENVIRONNEMENT CONDA !"
echo ""

# Lancer Django
echo "🚀 Lancement de Django..."
echo "💡 Le serveur sera accessible sur http://127.0.0.1:8000/"
echo "💡 Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

python manage.py runserver 127.0.0.1:8000
