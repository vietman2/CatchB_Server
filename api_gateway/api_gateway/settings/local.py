from .base import * # pylint: disable=W0401,W0614

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# allow only localhost
ALLOWED_HOSTS = ['e85c-147-47-133-18.ngrok-free.app']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

SERVICE_URLS = {
    'calendar_service':         'http://localhost:8001',
    'community_service':        'http://localhost:8002',
    'payments_service':         'http://localhost:8003',
    'products_service':         'http://localhost:8004',
    'user_management_service':  'http://localhost:8005',
}

CORS_ALLOWED_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
