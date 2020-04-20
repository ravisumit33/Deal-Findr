import django_heroku
import os, sys
import dj_database_url
from credential_manager import decrypt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, 'deal_findr'))

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False 

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [ 
    'deal_findr.apps.DealFindrConfig',
    'phonenumber_field',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'
AUTH_USER_MODEL = 'deal_findr.CustomUser'
PHONENUMBER_DEFAULT_REGION = 'IN'

DATABASES = { 'default' : dj_database_url.config()}

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

AUTHENTICATION_BACKENDS = (
    ('django.contrib.auth.backends.ModelBackend'),
)

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_ROOT = 'static'
STATIC_URL = '/static/'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = decrypt.cred['EMAIL_HOST_USER'] 
EMAIL_HOST_PASSWORD = decrypt.cred['EMAIL_HOST_PASSWD'] 
EMAIL_PORT = 587
EMAIL_USE_TLS = True



LOGIN_URL = 'deal_findr:login'
LOGIN_REDIRECT_URL = 'deal_findr:home'
LOGOUT_REDIRECT_URL = 'deal_findr:home'

try:
    from mysite.local_settings import *
except Exception as e:
    pass

django_heroku.settings(locals(), logging=False)
