import os
from pathlib import Path

from environs import Env

env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SELF_STORAGE_URL = env.str('SELF_STORAGE_URL')

SECRET_KEY = env.str('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

INTERNAL_IPS = ['127.0.0.1', ]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',
    "phonenumber_field",
    'storages',
    'tinymce',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'main_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'storages', 'templates')],
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

WSGI_APPLICATION = 'main_app.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


AUTH_PASSWORD_VALIDATORS = [

]

AUTH_USER_MODEL = 'storages.CustomUser'

LOGOUT_REDIRECT_URL = "/"

AUTHENTICATION_BACKENDS = ['storages.backends.EmailBackend']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.yandex.ru'

EMAIL_PORT = 465

EMAIL_USE_SSL = True

# EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
#
# EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
#
# DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL')

YOOKASSA_SHOP_ID = env.str('YOOKASSA_SHOP_ID')

YOOKASSA_SECRET_KEY = env.str('YOOKASSA_SECRET_KEY')

YANDEX_IS_TEST = True

LANGUAGE_CODE = 'ru-ru'

PHONE_NUMBER_REGION = 'RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

TINYMCE_DEFAULT_CONFIG = {
    'content_css': STATIC_ROOT,
}

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
