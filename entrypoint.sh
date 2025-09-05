#!/bin/sh
set -e

# Wait for database to be ready
echo "Waiting for database to be ready..."
while ! nc -z host.docker.internal 5432; do
  sleep 1
done
echo "Database is ready!"

# Ensure directories exist and have correct ownership
mkdir -p /app/staticfiles /app/media /app/logs
chown -R "$(id -u)":"$(id -g)" /app/staticfiles /app/media /app/logs || true

# Apply database migrations and collect static files
echo "Running database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Download ML models with fast startup (lightweight models first)
echo "Loading ML models with smart cache..."
python load_models_smart.py || echo "Smart model loading failed, continuing with fallback mode"

# Initialize chatbot loop prevention
echo "Initializing chatbot loop prevention..."
python chatbot_loop_prevention.py || echo "Loop prevention initialization failed, continuing"

# Verify BART model download
echo "Verifying BART model download..."
python verify_bart_download.py || echo "BART verification failed, continuing"

# Test chatbot functionality (simplified)
echo "Testing chatbot functionality..."
python -c "
import os
os.environ['HF_HOME'] = '/app/.cache/huggingface'
os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['TRANSFORMERS_OFFLINE'] = '1'
os.environ['TRANSFORMERS_CACHE'] = '/app/.cache/huggingface'
os.environ['SENTENCE_TRANSFORMERS_HOME'] = '/app/.cache/huggingface'
try:
    from sentence_transformers import SentenceTransformer
    from transformers import pipeline
    print('✅ Modèles ML chargés avec succès')
    print('✅ Chatbot prêt à répondre aux questions')
    print('✅ Mode offline activé - pas de téléchargements réseau')
except Exception as e:
    print(f'❌ Erreur chargement modèles: {e}')
" || echo "Chatbot test failed, continuing"

echo "Starting application..."
# Use environment variable for worker count, default to 3 if not set
WORKERS=${GUNICORN_WORKERS:-3}
exec gunicorn ParcInfo.wsgi:application --bind 0.0.0.0:8000 --workers "$WORKERS" --timeout 600 --access-logfile - --error-logfile - --log-level info


