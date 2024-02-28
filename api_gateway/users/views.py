from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from core.permissions import IsSelf
from core.views import get_response

user_service_url = settings.SERVICE_URLS['user_management_service']

class SignUpView(APIView):
    def post(self, request):
        REQUEST_URL = f'{user_service_url}/api/users/register/'

        return get_response(request.headers, request.body, REQUEST_URL, 'POST')

class LoginView(APIView):
    def post(self, request):
        REQUEST_URL = f'{user_service_url}/api/login/'

        return get_response(request.headers, request.body, REQUEST_URL, 'POST')

class LogoutView(APIView):
    def post(self, request):
        REQUEST_URL = f'{user_service_url}/api/logout/'

        return get_response(request.headers, request.body, REQUEST_URL, 'POST')

class PasswordChangeView(APIView):
    def post(self, request):
        REQUEST_URL = f'{user_service_url}/api/users/password_change/'

        return get_response(request.headers, request.body, REQUEST_URL, 'POST')

class UserView(APIView):
    ## TODO: List 조회 구현 시 관리자만 가능하도록 권한 설정
    ## TODO: Partial Update 구현 시 본인만 가능하도록 권한 설정
    def get(self, request, **kwargs):
        uuid = kwargs.get('uuid', None)
        if not IsSelf.has_object_permission(None, request, None, uuid):
            return Response(
                {'message': '권한이 없습니다.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        REQUEST_URL = f'{user_service_url}/api/users/{uuid}/'

        return get_response(request.headers, request.body, REQUEST_URL, 'GET')

    def delete(self, request):
        uuid = request.query_params.get('uuid', None)
        if not IsSelf.has_object_permission(None, request, None, uuid):
            return Response(
                {'message': '권한이 없습니다.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        REQUEST_URL = f'{user_service_url}/api/users/{uuid}/'

        return get_response(request.headers, request.body, REQUEST_URL, 'DELETE')

class TokenView(APIView):
    def post(self, request):
        REQUEST_URL = f'{user_service_url}/api/token/refresh/'

        return get_response(request.headers, request.body, REQUEST_URL, 'POST')

class CouponRegisterView(APIView):
    def post(self, request):
        REQUEST_URL = f'{user_service_url}/api/coupons/register/'

        return get_response(request.headers, request.body, REQUEST_URL, 'POST')

class CouponStatusCheckView(APIView):
    def get(self, request):
        REQUEST_URL = f'{user_service_url}/api/coupons/status/'

        return get_response(request.headers, request.body, REQUEST_URL, 'GET', request.query_params)

class CouponView(APIView):
    ## TODO: 쿠폰 생성은 관리자, 코치, 시설주만 가능하도록 권한 설정
    def get(self, request):
        REQUEST_URL = f'{user_service_url}/api/coupons/'

        return get_response(request.headers, request.body, REQUEST_URL, 'GET', request.query_params)

class PointsView(APIView):
    def get(self, request):
        REQUEST_URL = f'{user_service_url}/api/points/'

        return get_response(request.headers, request.body, REQUEST_URL, 'GET', request.query_params)
