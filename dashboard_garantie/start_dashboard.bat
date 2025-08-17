@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM Script de démarrage automatique du Dashboard de Garanties ParcInfo
REM Usage: start_dashboard.bat [port]

REM Port par défaut
set PORT=%1
if "%PORT%"=="" set PORT=8501

echo 🚀 Démarrage du Dashboard de Garanties ParcInfo...
echo 📍 Port: %PORT%
echo 🌐 URL: http://localhost:%PORT%
echo.

REM Vérifier si le port est déjà utilisé
netstat -an | find ":%PORT%" | find "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo ⚠️  Le port %PORT% est déjà utilisé par un autre processus.
    echo 🔍 Processus utilisant le port %PORT% :
    netstat -an | find ":%PORT%"
    echo.
    echo 🛑 Arrêt du processus existant...
    taskkill /f /im python.exe >nul 2>&1
    timeout /t 2 /nobreak >nul
)

REM Vérifier que le fichier Python existe
if not exist "dashboard_garantie.py" (
    echo ❌ Erreur: Le fichier dashboard_garantie.py n'existe pas dans le répertoire actuel
    echo 📁 Répertoire actuel: %cd%
    pause
    exit /b 1
)

REM Démarrer le serveur Streamlit
echo ▶️  Démarrage du serveur Streamlit...
echo ⏳ Veuillez patienter quelques secondes...
echo.

python -m streamlit run dashboard_garantie.py --server.port %PORT% --server.headless true

echo.
echo 🛑 Serveur arrêté.
pause
