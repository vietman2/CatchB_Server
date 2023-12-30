import requests
from django.conf import settings
from django.views.decorators.http import require_POST
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

user_service_url = settings.SERVICE_URLS['user_management_service']

def get_response(request, url, method):
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=request.headers,
            data=request.body,
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

@require_POST
def signup(request):
    REQUEST_URL = f'{user_service_url}/api/users/register/'
    
    return get_response(request, REQUEST_URL, 'POST')

@require_POST
def login(request):
    REQUEST_URL = f'{user_service_url}/api/login/'

    return get_response(request, REQUEST_URL, 'POST')

@require_POST
def logout(request):
    REQUEST_URL = f'{user_service_url}/api/logout/'

    return get_response(request, REQUEST_URL, 'POST')
"""
@api_view(['POST'])
def change_password(request):
    REQUEST_URL = f'{user_service_url}/api/users/change_password/'

    return get_response(request, REQUEST_URL, 'POST')

@api_view(['POST'])
def reset_password(request):
    REQUEST_URL = f'{user_service_url}/api/password/reset/'

    return get_response(request, REQUEST_URL, 'POST')
"""