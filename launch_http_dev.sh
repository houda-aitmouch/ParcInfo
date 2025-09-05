#!/bin/bash

# Activate virtual environment
source rag_env/bin/activate

# Kill any existing Django server
pkill -f "python manage.py runserver"

# Wait a moment for the process to be killed
sleep 2

# Launch Django with HTTP
echo "Starting Django development server with HTTP..."
echo "Access the application at: http://127.0.0.1:8000/"
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver 127.0.0.1:8000
