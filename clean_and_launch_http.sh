#!/bin/bash

echo "=== ParcInfo - Nettoyage Complet et Lancement HTTP ==="
echo ""

# Activer l'environnement virtuel
echo "1. Activation de l'environnement virtuel..."
source rag_env/bin/activate

# Arrêter TOUS les processus Django et Python
echo "2. Arrêt complet de tous les processus Django..."
pkill -f "python manage.py" 2>/dev/null
pkill -f "runserver" 2>/dev/null
pkill -f "uvicorn" 2>/dev/null
pkill -f "gunicorn" 2>/dev/null

# Attendre que tous les processus se terminent
sleep 5

# Vérification finale
echo "3. Vérification qu'aucun processus ne tourne..."
if pgrep -f "python manage.py" > /dev/null; then
    echo "   ⚠️  Forçage de l'arrêt des processus restants..."
    pkill -9 -f "python manage.py" 2>/dev/null
    sleep 2
fi

# Vérifier qu'aucun processus ne tourne
if pgrep -f "python manage.py" > /dev/null; then
    echo "   ❌ Impossible d'arrêter tous les processus Django"
    echo "   Veuillez redémarrer votre terminal et réessayer"
    exit 1
else
    echo "   ✅ Tous les processus Django arrêtés"
fi

# Nettoyer les fichiers temporaires
echo "4. Nettoyage des fichiers temporaires..."
rm -rf staticfiles/ 2>/dev/null
rm -rf __pycache__/ 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null

# Vérifier les dépendances
echo "5. Vérification des dépendances..."
python manage.py check --database default

# Lancer le serveur HTTP sur un port différent pour éviter les conflits
echo ""
echo "6. Lancement du serveur Django en HTTP (port 8080)..."
echo "   🌐 URL d'accès: http://127.0.0.1:8080/"
echo "   📝 Logs: Regardez la console pour les messages"
echo "   ⏹️  Arrêt: Ctrl+C"
echo ""
echo "=== IMPORTANT ==="
echo "Si vous utilisez un navigateur :"
echo "1. Fermez TOUS les onglets de localhost:8000"
echo "2. Videz le cache du navigateur (Cmd+Shift+R sur Mac)"
echo "3. Ou utilisez un mode navigation privée"
echo "4. Accédez à: http://127.0.0.1:8080/"
echo "=================="
echo ""

python manage.py runserver 127.0.0.1:8080
