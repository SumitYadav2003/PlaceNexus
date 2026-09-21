"""
Django settings for PlaceNexus.

All environment-specific values come from environment variables, so the same
code runs locally (values from .env), in Docker, and on Render.
"""

from pathlib import Path
import os

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Loads .env for local development. On Render/Docker there is no .env file,
# so this does nothing and real environment variables are used instead.
load_dotenv(BASE_DIR / '.env')


def env_bool(name, default=False):
    return os.getenv(name, str(default)).strip().lower() in ('1', 'true', 'yes', 'on')


def env_list(name, default=''):
    return [item.strip() for item in os.getenv(name, default).split(',') if item.strip()]


# ==========================================
# SECURITY
# ==========================================

SECRET_KEY = os.getenv('SECRET_KEY')

# Safe by default: DEBUG is only on when you explicitly set DEBUG=True
DEBUG = env_bool('DEBUG', False)

ALLOWED_HOSTS = env_list('ALLOWED_HOSTS', 'localhost,127.0.0.1')
CSRF_TRUSTED_ORIGINS = env_list('CSRF_TRUSTED_ORIGINS')

# Render sets this automatically (e.g. placenexus.onrender.com)
RENDER_EXTERNAL_HOSTNAME = os.getenv('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')

# HTTPS-only cookies in production. Set HTTPS_ONLY=False if you test a
# non-debug build over plain http://localhost (e.g. in Docker).
HTTPS_ONLY = env_bool('HTTPS_ONLY', not DEBUG)

if HTTPS_ONLY:
    # Render terminates HTTPS at its proxy and forwards this header
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# ==========================================
# APPLICATIONS
# ==========================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'anymail',

    'accounts',
    'profiles',
    'placements',
    'applications',
    'ai_module',
]

# ==========================================
# MIDDLEWARE
# ==========================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# ==========================================
# TEMPLATES
# ==========================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [
            BASE_DIR / "templates",
        ],

        'APP_DIRS': True,

        'OPTIONS': {

            'context_processors': [

                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',

            ],

        },

    },

]

WSGI_APPLICATION = 'config.wsgi.application'

# ==========================================
# DATABASE
# ==========================================
# On Render: set DATABASE_URL (from your Render Postgres).
# Locally: keep using the DB_* values in .env.

if os.getenv('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.parse(
            os.getenv('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
        }
    }

# ==========================================
# PASSWORD VALIDATORS
# ==========================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ==========================================
# INTERNATIONALIZATION
# ==========================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# ==========================================
# STATIC FILES (served by WhiteNoise)
# ==========================================

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# ==========================================
# MEDIA FILES (user uploads)
# ==========================================
# Local disk by default. If AWS_STORAGE_BUCKET_NAME is set, all uploads
# (resumes, photos, logos, post images) go to a PRIVATE S3 bucket and are
# served through short-lived signed URLs.

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': (
            'django.contrib.staticfiles.storage.StaticFilesStorage'
            if DEBUG
            else 'whitenoise.storage.CompressedManifestStaticFilesStorage'
        ),
    },
}

AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')

if AWS_STORAGE_BUCKET_NAME:
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    # Must match the region your bucket was created in
    AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'eu-west-2')
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_S3_ADDRESSING_STYLE = 'virtual'
    AWS_QUERYSTRING_AUTH = True        # private bucket, signed URLs
    AWS_QUERYSTRING_EXPIRE = 3600      # links valid for 1 hour
    AWS_S3_FILE_OVERWRITE = False      # never overwrite a file with the same name

    STORAGES['default'] = {
        'BACKEND': 'storages.backends.s3.S3Storage',
    }

# ==========================================
# LOGIN / LOGOUT
# ==========================================

LOGIN_URL = "/login/"

LOGIN_REDIRECT_URL = "/"

LOGOUT_REDIRECT_URL = "/login/"

# ==========================================
# PASSWORD RESET
# ==========================================

PASSWORD_RESET_TIMEOUT = 3600

# ==========================================
# EMAIL
# ==========================================
# Render's free tier blocks SMTP ports, so in production we send through
# Brevo's HTTP API (BREVO_API_KEY). Locally you can keep using Gmail SMTP,
# and with neither configured emails are printed to the console.

BREVO_API_KEY = os.getenv('BREVO_API_KEY')

if BREVO_API_KEY:
    EMAIL_BACKEND = "anymail.backends.brevo.EmailBackend"
    ANYMAIL = {
        "BREVO_API_KEY": BREVO_API_KEY,
    }
elif os.getenv('EMAIL_HOST_USER'):
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# With Brevo this must be a sender address you have verified in Brevo
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL') or os.getenv('EMAIL_HOST_USER') or 'noreply@localhost'

SERVER_EMAIL = DEFAULT_FROM_EMAIL

# ==========================================
# LOGGING (so errors show up in Render's log viewer)
# ==========================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': os.getenv('LOG_LEVEL', 'INFO'),
    },
}

# ==========================================
# DEFAULT PRIMARY KEY
# ==========================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"