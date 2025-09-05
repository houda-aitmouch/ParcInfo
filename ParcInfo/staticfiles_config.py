"""
Configuration spécifique pour les fichiers statiques Django
"""

import os
from pathlib import Path

# Configuration des fichiers statiques
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'staticfiles')

# Répertoires contenant les fichiers statiques
STATICFILES_DIRS = [
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'),
]

# Types de fichiers statiques reconnus
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Configuration pour le développement
if os.getenv('DEBUG', 'True').lower() == 'true':
    # En développement, servir depuis STATICFILES_DIRS
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
else:
    # En production, utiliser le stockage compilé
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Headers pour les fichiers statiques
STATICFILES_HEADERS = {
    '*.css': {
        'Cache-Control': 'public, max-age=31536000',
        'Content-Type': 'text/css',
    },
    '*.js': {
        'Cache-Control': 'public, max-age=31536000',
        'Content-Type': 'application/javascript',
    },
    '*.png': {
        'Cache-Control': 'public, max-age=31536000',
        'Content-Type': 'image/png',
    },
    '*.jpg': {
        'Cache-Control': 'public, max-age=31536000',
        'Content-Type': 'image/jpeg',
    },
    '*.ico': {
        'Cache-Control': 'public, max-age=31536000',
        'Content-Type': 'image/x-icon',
    },
}
