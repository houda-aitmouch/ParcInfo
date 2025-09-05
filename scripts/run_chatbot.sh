#!/usr/bin/env sh
set -e

# Assurer le contexte Django pour le chatbot
export PYTHONUNBUFFERED=1
export DJANGO_SETTINGS_MODULE=ParcInfo.settings
export PYTHONPATH=${PYTHONPATH:-/app}

exec python scripts/start_chatbot.py


