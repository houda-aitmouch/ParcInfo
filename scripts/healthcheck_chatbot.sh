#!/usr/bin/env sh

# Healthcheck minimal du chatbot
# Retourne 0 si Redis répond (à adapter selon votre implémentation)
redis-cli -h redis ping | grep -q PONG
exit $?


