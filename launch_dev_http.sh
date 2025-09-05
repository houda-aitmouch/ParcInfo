#!/bin/bash

echo "=== ParcInfo - Lancement Serveur de Développement HTTP ==="
echo ""

# Activer l'environnement virtuel
echo "1. Activation de l'environnement virtuel..."
source rag_env/bin/activate

# Arrêter tous les processus Django existants
echo "2. Arrêt des processus Django existants..."
pkill -f "python manage.py" 2>/dev/null
sleep 3

# Vérifier qu'aucun processus ne tourne
if pgrep -f "python manage.py" > /dev/null; then
    echo "   ⚠️  Forçage de l'arrêt des processus restants..."
    pkill -9 -f "python manage.py" 2>/dev/null
    sleep 2
fi

# Vérifier les dépendances
echo "3. Vérification des dépendances..."
python manage.py check --settings=ParcInfo.settings_dev

# Lancer le serveur avec la configuration de développement
echo ""
echo "4. Lancement du serveur Django en mode développement..."
echo "   🌐 URL d'accès: http://127.0.0.1:8000/"
echo "   🔧 Configuration: ParcInfo.settings_dev"
echo "   📝 Logs: Regardez la console pour les messages"
echo "   ⏹️  Arrêt: Ctrl+C"
echo ""
echo "=== Démarrage du serveur ==="
echo ""

python manage.py runserver 127.0.0.1:8000 --settings=ParcInfo.settings_dev
