from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from core.permissions import IsLoggedIn
from core.views import get_response

payments_service_url = settings.SERVICE_URLS['payments_service']

class BankView(APIView):
    def get(self, request):
        if not IsLoggedIn().has_permission(request, self):
            return Response(
                {'message': '로그인이 필요합니다.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        REQUEST_URL = f'{payments_service_url}/api/banks/'

        return get_response(request.headers, request.body, REQUEST_URL, 'GET')
