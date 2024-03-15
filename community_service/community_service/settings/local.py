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

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME = 'catchb.media'
AWS_S3_ENDPOINT_URL = 'https://kr.object.ncloudstorage.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
    'ACL': 'public-read',
}

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = 'https://kr.object.ncloudstorage.com/catchb.media/'
