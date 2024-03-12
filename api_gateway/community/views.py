from django.conf import settings
from rest_framework.views import APIView

from core.views import get_response

community_service_url = settings.SERVICE_URLS['community_service']

class TagView(APIView):
    def get(self, request):
        REQUEST_URL = f'{community_service_url}/api/tags/'

        return get_response(request.headers, request.body, REQUEST_URL, 'GET')

class ImageView(APIView):
    def post(self, request):
        REQUEST_URL = f'{community_service_url}/api/images/'

        return get_response(request.headers, request.body, REQUEST_URL, 'POST')
