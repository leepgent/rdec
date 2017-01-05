"""
Django settings for rdec project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('RDEC_SECRET_KEY', 'ah_f*z03ogus3mzgno)a)(!0!&hd$0(r*$ld78tqmtdi-t96%%')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (os.environ.get('RDEC_DEBUG', 'False') == 'True')


ALLOWED_HOSTS = os.environ.get('RDEC_ALLOWED_HOSTS', '').split()

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')


INSTALLED_APPS = []
MIDDLEWARE = []

# Storage. Use S3 or fall back to Whitenoise; undefined behaviour for media files in that case!
if AWS_ACCESS_KEY_ID:
    INSTALLED_APPS.extend([
        'storages'
    ])

    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_MEDIA_BUCKET_NAME = os.environ.get('AWS_MEDIA_BUCKET_NAME')

    AWS_S3_FILE_OVERWRITE = False

    DEFAULT_FILE_STORAGE = 's3storages.MediaRootS3BotoStorage'
    STATICFILES_STORAGE = 's3storages.StaticRootS3BotoStorage'

else:
    INSTALLED_APPS.extend([
        'whitenoise.runserver_nostatic',
    ])
    MIDDLEWARE.extend([
        'whitenoise.middleware.WhiteNoiseMiddleware'
    ])
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


INSTALLED_APPS.extend([
    'django.contrib.admin',
    'django.contrib.auth',
    'accounts',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rdec'
])

MIDDLEWARE.extend([
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
])


ROOT_URLCONF = 'rdecsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'rdec.context_processors.league_name'
            ],
        },
    },
]

WSGI_APPLICATION = 'rdecsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///rdec.db')
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

LOGIN_URL = '/login/'


LEAGUE_NAME = os.environ.get('RDEC_LEAGUE_NAME', 'Default City Derby')
RECENT_EVENT_CUTOFF_DAYS = os.environ.get('RDEC_RECENT_EVENT_CUTOFF_DAYS', 10)

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME')
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = os.environ.get('RDEC_MAIL_FROM_ADDRESS')
AUTH_USER_MODEL = 'accounts.User'


