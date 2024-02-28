from .base import * # pylint: disable=W0401,W0614

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config("PRODUCTS_DB_NAME"),
        'USER': config("DB_USER"),
        'PASSWORD': config("DB_PASSWORD"),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

NAVER_CLIENT_ID = config("NAVER_API_KEY_ID")
NAVER_CLIENT_SECRET = config("NAVER_API_KEY")
