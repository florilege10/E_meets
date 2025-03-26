from pathlib import Path
import os
import environ

import dj_database_url


# Initialiser les variables d'environnement
env = environ.Env()




BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(env_file=str(BASE_DIR / '.env'))

# ✅ Clé secrète depuis .env

SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')  # Ne jamais laisser une valeur par défaut en prod !


# ✅ Mode debug depuis .env
DEBUG = env.bool('DEBUG', default=False)

# ✅ Hôtes autorisés
ALLOWED_HOSTS = ['meets-api.onrender.com', 'localhost', '127.0.0.1']

# ✅ Applications Django de base
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # ✅ Applications tierces
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',

    # ✅ Authentification
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    "whitenoise.runserver_nostatic",

    # ✅ Apps locales
    'makutano', 
]

# ✅ Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Middleware django-allauth
    'allauth.account.middleware.AccountMiddleware',
]

# ✅ Configuration des templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ✅ Configuration de la base de données avec ElephantSQL
# Replace the SQLite DATABASES configuration with PostgreSQL:
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv("DATABASE_URL"),  # Récupère l'URL de la base depuis Render
        conn_max_age=600
    )
}


# ✅ Gestion des fichiers statiques
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ✅ Gestion des fichiers médias
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# ✅ Modèle utilisateur personnalisé
AUTH_USER_MODEL = 'makutano.Profile'

# ✅ Paramètres d'authentification
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# ✅ Configuration de Django Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# ✅ Configuration CORS
CORS_ALLOW_ALL_ORIGINS = True  # À ajuster en production

# ✅ Configuration e-mail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='smtp.example.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='your-email@example.com')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='your-password')

# ✅ WSGI
WSGI_APPLICATION = 'Meets.wsgi.application'


ROOT_URLCONF = 'Meets.urls'  # Remplace 'Meets' par le nom de ton projet si c'est différent




if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True