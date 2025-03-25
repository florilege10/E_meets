from pathlib import Path
import os
import environ

# Initialiser les variables d'environnement
env = environ.Env()
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ Clé secrète depuis .env
SECRET_KEY = env('SECRET_KEY')

# ✅ Mode debug depuis .env
DEBUG = env.bool('DEBUG', default=False)

# ✅ Hôtes autorisés
ALLOWED_HOSTS = ['.vercel.app', '.now.sh', 'localhost', '127.0.0.1']

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
DATABASES = {
    'default': {
        'ENGINE': env('DB_ENGINE', default='django.db.backends.postgresql_psycopg2'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

# ✅ Gestion des fichiers statiques
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
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
