@echo off
chcp 65001 >nul
echo 🚀 Lancement du Dashboard Garantie ParcInfo
echo =============================================

REM Vérifier si l'environnement virtuel existe
if not exist "env" (
    echo 📦 Création de l'environnement virtuel...
    python -m venv env
)

REM Activer l'environnement virtuel
echo 🔧 Activation de l'environnement virtuel...
call env\Scripts\activate.bat

REM Installer les dépendances
echo 📥 Installation des dépendances...
pip install -r requirements.txt

REM Lancer le dashboard
echo 🌐 Lancement du dashboard...
echo 📍 Le dashboard sera accessible à l'adresse: http://localhost:8501
echo 🔄 Appuyez sur Ctrl+C pour arrêter le dashboard
echo.

REM Aller dans le dossier dashboard_garantie et lancer le dashboard
cd dashboard_garantie
streamlit run dashboard_garantie.py --server.port 8501 --server.address 0.0.0.0

pause
