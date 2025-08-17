#!/bin/bash

# Script de démarrage automatique pour ParcInfo
# À placer dans ~/Library/LaunchAgents/ pour un démarrage automatique

# Chemin vers le projet
PROJECT_PATH="/Users/HouDa/PycharmProjects/ParcInfo"

# Aller dans le répertoire du projet
cd "$PROJECT_PATH"

# Lancer le script de démarrage
./launch_project.sh
