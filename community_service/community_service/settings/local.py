from .base import * # pylint: disable=W0401,W0614

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }

    #'default': {
    #    'ENGINE': 'django.db.backends.postgresql',
    #    'NAME': config("COMMUNITY_DB_NAME"),
    #    'USER': config("DB_USER"),
    #    'PASSWORD': config("DB_PASSWORD"),
    #    'HOST': 'localhost',
    #    'PORT': '5433',
    #}
}
