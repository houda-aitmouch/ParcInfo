#!/bin/bash

# Activate virtual environment
source rag_env/bin/activate

# Create SSL certificates directory if it doesn't exist
mkdir -p ssl_certs

# Generate self-signed SSL certificate if it doesn't exist
if [ ! -f ssl_certs/localhost.crt ] || [ ! -f ssl_certs/localhost.key ]; then
    echo "Generating SSL certificates..."
    openssl req -x509 -newkey rsa:4096 -keyout ssl_certs/localhost.key -out ssl_certs/localhost.crt -days 365 -nodes -subj "/C=FR/ST=State/L=City/O=Organization/CN=localhost"
fi

# Kill any existing Django server
pkill -f "python manage.py runserver"

# Wait a moment for the process to be killed
sleep 2

# Install required packages if not already installed
pip install django-extensions Werkzeug

# Launch Django with HTTPS support
echo "Starting Django development server with HTTPS..."
echo "Access the application at: https://127.0.0.1:8000/"
echo "Note: You may need to accept the self-signed certificate in your browser"
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver_plus --cert-file ssl_certs/localhost.crt --key-file ssl_certs/localhost.key 127.0.0.1:8000
