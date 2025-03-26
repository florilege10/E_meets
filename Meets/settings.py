from pathlib import Path
import os
import environ
import dj_database_url

# Initialisation des variables d'environnement
env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(env_file=str(BASE_DIR / '.env'))

# Configuration de base
SECRET_KEY = os.getenv('SECRET_KEY')  # Obligatoire en production
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = ['makutano.onrender.com', 'localhost', '127.0.0.1']

# Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Applications tierces
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'whitenoise.runserver_nostatic',
    
    # Application locale
    'makutano',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuration de la base de données
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600
    )
}

# URLs et WSGI
ROOT_URLCONF = 'Meets.urls'
WSGI_APPLICATION = 'Meets.wsgi.application'

# Authentification
AUTH_USER_MODEL = 'makutano.Profile'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Plus permissif pour l'inscription
    ],
}
# ==============================================
# Configuration CORS et Sécurité
# ==============================================

# CORS (Cross-Origin Resource Sharing)
CORS_ALLOWED_ORIGINS = [
    "https://makutano.onrender.com",
    "http://localhost:3000",
    "http://127.0.0.1:3000",  # Pour le développement local
]
CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']
CORS_ALLOW_CREDENTIALS = True

# Configuration CSRF
CSRF_TRUSTED_ORIGINS = [
    'https://makutano.onrender.com',
    'https://*.onrender.com'
]
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = False  # Nécessaire pour les APIs
CSRF_USE_SESSIONS = False
CSRF_COOKIE_SECURE = True  # HTTPS seulement

# ==============================================
# Configuration des fichiers statiques et média
# ==============================================

# Fichiers statiques
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Dossier source pour collectstatic

# Configuration WhiteNoise optimisée
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_MAX_AGE = 31536000  # Cache pour 1 an
WHITENOISE_USE_FINDERS = True
WHITENOISE_MANIFEST_STRICT = False

# Fichiers média
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ==============================================
# Sécurité renforcée
# ==============================================

if not DEBUG:
    # HTTPS
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Cookies
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Protection diverses
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'

# Internationalisation
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True