from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from dj_rest_auth.views import LoginView, LogoutView

from .serializers import (
    UserRegisterSerializer, UserSerializer,
    PasswordChangeSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer,
)
from .models import CustomUser
from .permissions import IsActive

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)

class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    @extend_schema(exclude=True)
    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(summary="본인 회원 정보 조회", tags=["회원 관리"])
    def retrieve(self, request, *args, **kwargs):
        user = CustomUser.objects.get(uuid=kwargs['pk'])

        if not IsActive().has_object_permission(request, self, self.get_object()):
            return Response(data={
                "errors": "비활성화된 계정입니다.",
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(summary="회원 정보 리스트 조회", tags=["회원 관리"])
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(summary="회원 탈퇴", tags=["회원 관리"])
    def destroy(self, request, *args, **kwargs):
        if not IsActive().has_object_permission(request, self, self.get_object()):
            return Response(data={
                "errors": "이미 탈퇴한 계정입니다.",
            }, status=status.HTTP_403_FORBIDDEN)

        user = self.get_object()
        CustomUser.objects.delete_user(user)
        user.save()

        return Response(data={"message": "탈퇴되었습니다."}, status=status.HTTP_200_OK)

    @extend_schema(summary="회원 정보 수정", tags=["회원 관리"])
    def partial_update(self, request, *args, **kwargs):
        if not IsActive().has_object_permission(request, self, self.get_object()):
            return Response(data={
                "errors": "비활성화된 계정입니다.",
            }, status=status.HTTP_403_FORBIDDEN)

        user = self.get_object()

        serializer = UserSerializer(user, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(data={
                "errors": e.detail,
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

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
        data = {
            "message": "회원가입이 완료되었습니다. 로그인해주세요."
        }
        return Response(data=data, status=status.HTTP_201_CREATED, headers=headers)

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
        # pylint: disable=unused-argument
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
