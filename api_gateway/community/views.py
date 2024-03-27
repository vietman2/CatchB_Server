from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from core.permissions import IsLoggedIn, get_user_info
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

    def get(self, request):
        REQUEST_URL = f'{community_service_url}/api/posts/'

        return get_response(
            request.headers,
            request.body,
            REQUEST_URL,
            'GET',
            request.query_params
        )

class PostDetailView(APIView):
    def get(self, request, pk):
        REQUEST_URL = f'{community_service_url}/api/posts/{pk}/'

        if not IsLoggedIn().has_permission(request, self):
            return get_response(request.headers, request.body, REQUEST_URL, 'GET')

        uuid = get_user_info(request)['user_id']

        return get_response(request.headers, request.body, REQUEST_URL, 'GET', {'uuid': uuid})

class PostLikeView(APIView):
    def post(self, request, pk):
        if not IsLoggedIn().has_permission(request, self):
            return Response(
                {'message': '로그인이 필요합니다.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        REQUEST_URL = f'{community_service_url}/api/posts/{pk}/like/'

        return get_response(request.headers, request.body, REQUEST_URL, 'POST')

class PostDislikeView(APIView):
    def post(self, request, pk):
        if not IsLoggedIn().has_permission(request, self):
            return Response(
                {'message': '로그인이 필요합니다.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        REQUEST_URL = f'{community_service_url}/api/posts/{pk}/dislike/'

        return get_response(request.headers, request.body, REQUEST_URL, 'POST')

class CommentView(APIView):
    def post(self, request):
        if not IsLoggedIn().has_permission(request, self):
            return Response(
                {'message': '로그인이 필요합니다.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        REQUEST_URL = f'{community_service_url}/api/comments/'

        return get_response(request.headers, request.body, REQUEST_URL, 'POST')

    def get(self, request):
        REQUEST_URL = f'{community_service_url}/api/comments/'

        if not IsLoggedIn().has_permission(request, self):
            return get_response(
                request.headers,
                request.body,
                REQUEST_URL,
                'GET',
                request.query_params
            )
        
        uuid = get_user_info(request)['user_id']
        params = request.query_params.copy()
        params['user_uuid'] = uuid

        return get_response(
            request.headers,
            request.body,
            REQUEST_URL,
            'GET',
            params
        )

class CommentLikeView(APIView):
    def post(self, request, pk):
        if not IsLoggedIn().has_permission(request, self):
            return Response(
                {'message': '로그인이 필요합니다.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        REQUEST_URL = f'{community_service_url}/api/comments/{pk}/like/'

        return get_response(request.headers, request.body, REQUEST_URL, 'POST')

class CommentDislikeView(APIView):
    def post(self, request, pk):
        if not IsLoggedIn().has_permission(request, self):
            return Response(
                {'message': '로그인이 필요합니다.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        REQUEST_URL = f'{community_service_url}/api/comments/{pk}/dislike/'

        return get_response(request.headers, request.body, REQUEST_URL, 'POST')
