from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from dj_rest_auth.views import LoginView, LogoutView

from .serializers import (
    UserRegisterSerializer, UserProfileSerializer, CoachProfileSerializer,
    PasswordChangeSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer,
)
from .models import CustomUser

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)

class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated,]
    http_method_names = ['get', 'post', 'head', 'options']

    @extend_schema(summary="회원 가입", tags=["회원 관리"])
    @action(
        detail=False,
        methods=['post'],
        permission_classes=[AllowAny,],
        serializer_class=UserRegisterSerializer,
    )
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.validate_passwords(serializer.validated_data)
        except ValidationError as e:
            return Response(data={
                "errors": e.detail,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(summary="비밀번호 변경", tags=["회원 관리"])
    @action(
        detail=False,
        methods=['post'],
        permission_classes=[IsAuthenticated,],
        serializer_class=PasswordChangeSerializer,
    )
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(data={
                "errors": e.detail,
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    """
    @extend_schema(summary="코치 등록", tags=["회원 관리"])
    @action(
        detail=False,
        methods=['post'],
        permission_classes=[IsAuthenticated,],
        serializer_class=CoachProfileSerializer,
    )
    def coach(self, request):
        serializer = CoachProfileSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(data={
                "errors": e.detail,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    """

class MyLoginView(LoginView):
    @extend_schema(summary="로그인", tags=["회원 관리"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class MyLogoutView(LogoutView):
    serializer_class = None
    http_method_names = ['post', 'head', 'options']

    @extend_schema(summary="로그아웃", tags=["회원 관리"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes=[AllowAny,]
    throttle_scope = 'dj_rest_auth'
    http_method_names = ['post', 'head', 'options']

    @extend_schema(summary="비밀번호 재설정", tags=["회원 관리"])
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(data={
                "errors": e.detail,
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class PasswordResetConfirmView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes=[AllowAny,]
    throttle_scope = 'dj_rest_auth'

    @extend_schema(summary="비밀번호 재설정 확인", tags=["회원 관리"])
    def post(self, request, *args, **kwargs):
        request_data_copy = request.data.copy()
        request_data_copy['uid'] = kwargs['uidb64']
        request_data_copy['token'] = kwargs['token']
        serializer = self.get_serializer(data=request_data_copy)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(data={
                "errors": e.detail,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
