from .settings import *  # noqa

# Development-specific overrides to ensure pure HTTP and no SSL redirects

# Force DEBUG in dev
DEBUG = True

# Allow local hosts
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '0.0.0.0',
]

# Disable all HTTPS-related enforcement explicitly
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = None
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Remove SecurityMiddleware completely to prevent any HTTPS redirects
MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Optional: Verbose logging for debugging
LOGGING['loggers']['django'] = {
    'handlers': ['console'],
    'level': 'DEBUG',
    'propagate': True,
}


