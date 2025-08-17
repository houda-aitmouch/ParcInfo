@echo off
REM Script pour lancer Django et Streamlit simultanément
REM ParcInfo - Dashboard de Garanties

echo 🚀 Lancement du projet ParcInfo...
echo 📍 Port Django: 8000
echo 📍 Port Streamlit: 8501
echo.

REM Vérifier si les ports sont utilisés
echo 🔍 Vérification des ports...

netstat -an | find ":8000" | find "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo ❌ Port 8000 déjà utilisé
    echo    Arrêt des processus Django existants...
    taskkill /f /im python.exe >nul 2>&1
    timeout /t 2 >nul
)

netstat -an | find ":8501" | find "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo ❌ Port 8501 déjà utilisé
    echo    Arrêt des processus Streamlit existants...
    taskkill /f /im python.exe >nul 2>&1
    timeout /t 2 >nul
)

echo ✅ Ports disponibles
echo.

REM Lancer Django en arrière-plan
echo 🌐 Démarrage du serveur Django...
start "Django Server" cmd /c "python manage.py runserver 8000"
echo ✅ Django démarré
echo    URL: http://localhost:8000
echo.

REM Attendre un peu pour que Django démarre
timeout /t 3 >nul

REM Lancer Streamlit en arrière-plan
echo 📊 Démarrage du serveur Streamlit...
cd dashboard_garantie
start "Streamlit Server" cmd /c "python -m streamlit run dashboard_garantie.py --server.port 8501 --server.headless true"
cd ..
echo ✅ Streamlit démarré
echo    URL: http://localhost:8501
echo.

REM Attendre un peu pour que Streamlit démarre
timeout /t 5 >nul

echo 🎉 Projet ParcInfo lancé avec succès !
echo.
echo 📋 URLs disponibles :
echo    🌐 Django: http://localhost:8000
echo    📊 Dashboard Garanties: http://localhost:8501
echo.
echo 💡 Les serveurs sont maintenant actifs dans des fenêtres séparées
echo    Pour les arrêter, fermez les fenêtres correspondantes
echo.

pause
