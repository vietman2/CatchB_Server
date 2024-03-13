from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from core.permissions import IsLoggedIn
from core.views import get_response

community_service_url = settings.SERVICE_URLS['community_service']

class TagView(APIView):
    def get(self, request):
        REQUEST_URL = f'{community_service_url}/api/tags/'

        return get_response(request.headers, request.body, REQUEST_URL, 'GET')

class ImageView(APIView):
    def post(self, request):
        if not IsLoggedIn().has_permission(request, self):
            return Response(
                {'message': '로그인이 필요합니다.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        REQUEST_URL = f'{community_service_url}/api/images/'

        return get_response(request.headers, request.body, REQUEST_URL, 'POST')

class PostView(APIView):
    def post(self, request):
        if not IsLoggedIn().has_permission(request, self):
            return Response(
                {'message': '로그인이 필요합니다.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        REQUEST_URL = f'{community_service_url}/api/posts/'

        return get_response(request.headers, request.body, REQUEST_URL, 'POST')
