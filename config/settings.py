import os
from pathlib import Path
import cloudinary
import dj_database_url
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1').split(',')

# Security / CSRF configuration for production
CSRF_TRUSTED_ORIGINS = [
    f'https://{host}' for host in ALLOWED_HOSTS if host != '127.0.0.1'
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',  # Positions above staticfiles for media overriding
    'django.contrib.staticfiles',
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'channels',
    'cloudinary',
    # Project apps
    'users',
    'feed',
    'messaging',
    'resources',
    'events',
    'marketplace',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Crucial for serving admin static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Shared templates folder
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }
]

ASGI_APPLICATION = 'config.asgi.application'

# Channels / Real-time configuration
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [os.getenv('REDIS_URL', 'redis://127.0.0.1:6379')],
        },
    },
}

# Database configuration (PostgreSQL)
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DATABASE_NAME'),
            'USER': os.getenv('DATABASE_USER'),
            'PASSWORD': os.getenv('DATABASE_PASSWORD'),
            'HOST': os.getenv('DATABASE_HOST'),
            'PORT': os.getenv('DATABASE_PORT'),
        }
    }

# Authentication URLs
LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/users/login/'
AUTH_USER_MODEL = 'users.CustomUser'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.getenv('STATIC_ROOT', str(BASE_DIR / 'staticfiles'))

# Keep this directory explicitly defined to ensure local files are gathered seamlessly
STATICFILES_DIRS = [BASE_DIR / 'static']

# Fallback environment config check for WhiteNoise root matching
WHITENOISE_ROOT = STATIC_ROOT

# Media files (Cloudinary uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

# Separate storage engines for media vs static assets
STORAGES = {
    'default': {
        'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}
WHITENOISE_MANIFEST_STRICT = False

# REST Framework configurations
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'