from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from core.permissions import IsLoggedIn
from core.views import get_response

products_service_url = settings.SERVICE_URLS['products_service']

class FacilityView(APIView):
    def post(self, request):
        if not IsLoggedIn().has_permission(request, self):
            return Response(
                {'message': '로그인이 필요합니다.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        REQUEST_URL = f'{products_service_url}/api/facilities/'

        return get_response(request.headers, request.body, REQUEST_URL, 'POST')
    
    def get(self, request):
        REQUEST_URL = f'{products_service_url}/api/facilities/'

        return get_response(request.headers, request.body, REQUEST_URL, 'GET')

class FacilityInfoView(APIView):
    def post(self, request, uuid):
        if not IsLoggedIn().has_permission(request, self):
            return Response(
                {'message': '로그인이 필요합니다.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        REQUEST_URL = f'{products_service_url}/api/facilities/{uuid}/info/'

        return get_response(
            request.headers,
            request.body,
            REQUEST_URL,
            'POST'
        )

class RegionView(APIView):
    def get(self, request):
        REQUEST_URL = f'{products_service_url}/api/regions/'

        return get_response(
            request.headers,
            request.body,
            REQUEST_URL,
            'GET'
        )
