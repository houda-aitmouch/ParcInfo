#!/bin/bash

# Script de nettoyage du projet ParcInfo
echo "🧹 Nettoyage du projet ParcInfo..."

# Sauvegarde des fichiers importants
echo "💾 Sauvegarde des fichiers importants..."
mkdir -p backup-important-files
cp requirements.txt backup-important-files/
cp docker-compose.yml backup-important-files/
cp manage.py backup-important-files/
cp -r apps backup-important-files/
cp -r ParcInfo backup-important-files/
cp -r frontend backup-important-files/
cp -r templates backup-important-files/
cp -r static backup-important-files/

echo "🗑️ Suppression des fichiers inutiles..."

# Supprimer les fichiers de développement et tests
rm -f audit_vues_permissions.py
rm -f chatbot_loop_prevention.py
rm -f comparison_old_vs_new_diagram.py
rm -f correction_chatbot_baie.py
rm -f correction_chatbot_methods.py
rm -f debug_server.py
rm -f demo_chatbot_improvements.py
rm -f demo_corrections_chatbot.py
rm -f download_models_manual.py
rm -f download_models.py
rm -f enhanced_llm_prompt.py
rm -f enhanced_training_dataset.py
rm -f export_all_tables.py
rm -f export_chatbot_database*.py
rm -f export_database_schema*.py
rm -f extract_database_tables*.py
rm -f generate_backlog*.py
rm -f generate_uml_diagrams.py
rm -f generate_updated_bpmn_diagram.py
rm -f generate_workflow_diagram.py
rm -f launch_*.py
rm -f launch_*.sh
rm -f launch_*.bat
rm -f list_models.py
rm -f manage_rag.py
rm -f monitor_dashboard.py
rm -f setup_database.py
rm -f test_workflow_diagram.py
rm -f verify_bart_download.py

# Supprimer les fichiers de configuration inutiles
rm -f app.json
rm -f Procfile
rm -f railway.json
rm -f render.yaml
rm -f runtime.txt
rm -f com.parcinfo.startup.plist
rm -f entrypoint.sh
rm -f startup_parcinfo.sh

# Supprimer les fichiers de déploiement obsolètes
rm -f deploy_phase3.sh
rm -f build_with_retry.sh
rm -f clean_*.sh
rm -f setup_diagrams.sh

# Supprimer les fichiers de données temporaires
rm -f *.xlsx
rm -f *.csv
rm -f *.txt
rm -f *.log
rm -f *.sql
rm -f *.json
rm -f dump.rdb

# Supprimer les dossiers temporaires
rm -rf __pycache__
rm -rf backup/
rm -rf db/
rm -rf diagrammes_generes/
rm -rf docs/
rm -rf graphviz_env/
rm -rf logs/
rm -rf rag_env/
rm -rf retrained_bart_model/
rm -rf ssl_certs/
rm -rf storage/
rm -rf test_env/
rm -rf venv/
rm -rf venv_bpmn/
rm -rf venv_download/
rm -rf node_modules/
rm -rf staticfiles/

# Supprimer les fichiers de documentation obsolètes
rm -f DEPLOYMENT.md
rm -f DIGITALOCEAN_DEPLOYMENT.md
rm -f HEROKU_DEPLOYMENT.md
rm -f RAILWAY_*.md
rm -f RENDER_DEPLOYMENT.md
rm -f README_Diagramme_*.md
rm -f README_Workflow_*.md
rm -f RESUME_FINAL_*.md
rm -f OPTIMISATIONS_*.md
rm -f Interfaces_*.md
rm -f USER_STORIES_*.md
rm -f DATABASE_SETUP.md

# Supprimer les requirements inutiles
rm -f requirements_*.txt
rm -f requirements.minimal.txt

# Supprimer les scripts railway obsolètes
rm -f railway-start-*.sh

# Supprimer les fichiers de configuration nginx obsolètes
rm -f nginx.railway.conf

echo "✅ Nettoyage terminé !"
echo "📁 Fichiers importants sauvegardés dans : backup-important-files/"

echo ""
echo "📋 Fichiers conservés :"
echo "- manage.py (Django)"
echo "- requirements.txt (dépendances)"
echo "- docker-compose.yml (Docker)"
echo "- apps/ (applications Django)"
echo "- ParcInfo/ (configuration Django)"
echo "- frontend/ (React)"
echo "- templates/ (templates HTML)"
echo "- static/ (fichiers statiques)"
echo "- DOCKER_IMAGES.md (documentation Docker)"
echo "- AZURE_DEPLOYMENT.md (guide Azure)"
echo "- deploy.sh (script de déploiement)"
echo "- save-images.sh / restore-images.sh (sauvegarde images)"

echo ""
echo "🎯 Projet nettoyé et optimisé !"
