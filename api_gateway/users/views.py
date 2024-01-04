import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

user_service_url = settings.SERVICE_URLS['user_management_service']

def get_response(request, url, method):
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=request.headers,
            data=request.body,
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

@api_view(['POST'])
def refresh_token(request):
    REQUEST_URL = f'{user_service_url}/api/token/refresh/'

    return get_response(request, REQUEST_URL, 'POST')

@api_view(['GET'])
def get_user_profile(request, uuid):
    REQUEST_URL = f'{user_service_url}/api/users/{uuid}/'

    return get_response(request, REQUEST_URL, 'GET')

@api_view(['POST'])
def logout(request):
    REQUEST_URL = f'{user_service_url}/api/logout/'

    return get_response(request, REQUEST_URL, 'POST')

class LoginView(APIView):
    def post(self, request):
        REQUEST_URL = f'{user_service_url}/api/login/'

        return get_response(request, REQUEST_URL, 'POST')
