import requests
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

user_service_url = settings.SERVICE_URLS['user_management_service']

def get_response(request, url, method, query_params=None):
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=request.headers,
            data=request.body,
            params=query_params,
            timeout=10,
        )

        return Response(
            response.json(),
            status=response.status_code,
        )

    except requests.RequestException as e:
        return Response(
            {'message': str(e)},
            status=status.HTTP_502_BAD_GATEWAY,
        )

class SignUpView(APIView):
    def post(self, request):
        REQUEST_URL = f'{user_service_url}/api/users/register/'

        return get_response(request, REQUEST_URL, 'POST')

class LoginView(APIView):
    def post(self, request):
        REQUEST_URL = f'{user_service_url}/api/login/'

        return get_response(request, REQUEST_URL, 'POST')

class LogoutView(APIView):
    def post(self, request):
        REQUEST_URL = f'{user_service_url}/api/logout/'

        return get_response(request, REQUEST_URL, 'POST')

class UserView(APIView):
    def get(self, request):
        uuid = request.query_params.get('uuid', None)
        REQUEST_URL = f'{user_service_url}/api/users/{uuid}/'

        return get_response(request, REQUEST_URL, 'GET')

    def delete(self, request):
        uuid = request.query_params.get('uuid', None)
        REQUEST_URL = f'{user_service_url}/api/users/{uuid}/'

        return get_response(request, REQUEST_URL, 'DELETE')

class TokenView(APIView):
    def post(self, request):
        REQUEST_URL = f'{user_service_url}/api/token/refresh/'

        return get_response(request, REQUEST_URL, 'POST')

class CouponRegisterView(APIView):
    def post(self, request):
        REQUEST_URL = f'{user_service_url}/api/coupons/register/'

        return get_response(request, REQUEST_URL, 'POST')

class CouponStatusCheckView(APIView):
    def get(self, request):
        REQUEST_URL = f'{user_service_url}/api/coupons/status/'

        return get_response(request, REQUEST_URL, 'GET', request.query_params)

class CouponView(APIView):
    def get(self, request):
        REQUEST_URL = f'{user_service_url}/api/coupons/'

        return get_response(request, REQUEST_URL, 'GET', request.query_params)

class PointsView(APIView):
    def get(self, request):
        REQUEST_URL = f'{user_service_url}/api/points/'

        return get_response(request, REQUEST_URL, 'GET', request.query_params)
