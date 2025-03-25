from pathlib import Path
from decouple import config
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ Secrets et configuration sensible

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.environ.get("DEBUG") != "False"

ALLOWED_HOSTS = [".vercel.app", ".now.sh"]



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

    # ✅ Apps tierces pour l'authentification
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    "whitenoise.runserver_nostatic",

    # ✅ Tes applications locales
    'makutano', 
]

ROOT_URLCONF = 'Meets.urls'

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
    
    # Middleware de django-allauth
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

# ✅ Base de données (utiliser une DB externe en production comme PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # À remplacer par une DB de production comme PostgreSQL
    }
}

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

# ✅ Static & Media files
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# Utiliser un stockage externe pour les fichiers statiques et médias (par exemple AWS S3)
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_ROOT = BASE_DIR / "media"

# ✅ CORS Configuration
CORS_ALLOW_ALL_ORIGINS = True  # À ajuster en production pour limiter les origines autorisées

# ✅ Paramètres de l'email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-password'

# ✅ Configuration django-allauth
ACCOUNT_LOGIN_METHODS = ['email']
ACCOUNT_SIGNUP_FIELDS = ['email*', 'sexe', 'password1', 'password2']
#ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # Ou 'optional'



# ✅ Variables d'environnement pour configuration de la DB et autres
DATABASES['default'] = {
    'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3'),
    'NAME': config('DB_NAME', default=BASE_DIR / 'db.sqlite3'),
    'USER': config('DB_USER', default=''),
    'PASSWORD': config('DB_PASSWORD', default=''),
    'HOST': config('DB_HOST', default=''),
    'PORT': config('DB_PORT', default=''),
}

# api/settings.py
WSGI_APPLICATION = 'Meets.wsgi.app'