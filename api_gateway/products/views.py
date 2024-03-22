from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from core.permissions import IsLoggedIn
from core.views import get_response

products_service_url = settings.SERVICE_URLS['products_service']

class CoachView(APIView):
    def post(self, request):
        if not IsLoggedIn().has_permission(request, self):
            return Response(
                {'message': '로그인이 필요합니다.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        REQUEST_URL = f'{products_service_url}/api/coaches/'

        return get_response(request.headers, request.body, REQUEST_URL, 'POST')

    def get(self, request):
        REQUEST_URL = f'{products_service_url}/api/coaches/'

        return get_response(request.headers, request.body, REQUEST_URL, 'GET')

class CoachInfoView(APIView):
    def post(self, request, uuid):
        if not IsLoggedIn().has_permission(request, self):
            return Response(
                {'message': '로그인이 필요합니다.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        REQUEST_URL = f'{products_service_url}/api/coaches/{uuid}/info/'

        return get_response(
            request.headers,
            request.body,
            REQUEST_URL,
            'POST'
        )

    def get(self, request, uuid):
        REQUEST_URL = f'{products_service_url}/api/coaches/{uuid}/'

        return get_response(
            request.headers,
            request.body,
            REQUEST_URL,
            'GET'
        )

class CoachStatusView(APIView):
    def get(self, request):
        if not IsLoggedIn().has_permission(request, self):
            return Response(
                {'message': '로그인이 필요합니다.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        REQUEST_URL = f'{products_service_url}/api/coaches/status/'

        return get_response(
            request.headers,
            request.body,
            REQUEST_URL,
            'GET',
            request.query_params
        )

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

    def get(self, request, uuid):
        REQUEST_URL = f'{products_service_url}/api/facilities/{uuid}/'

        return get_response(
            request.headers,
            request.body,
            REQUEST_URL,
            'GET'
        )

class FacilityStatusView(APIView):
    def get(self, request):
        if not IsLoggedIn().has_permission(request, self):
            return Response(
                {'message': '로그인이 필요합니다.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        REQUEST_URL = f'{products_service_url}/api/facilities/status/'

        return get_response(
            request.headers,
            request.body,
            REQUEST_URL,
            'GET',
            request.query_params
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
