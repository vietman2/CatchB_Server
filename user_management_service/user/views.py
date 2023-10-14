from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import GenericAPIView

from .serializers import UserRegisterSerializer, PasswordChangeSerializer, PasswordResetSerializer

class RegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.validate_passwords(serializer.validated_data)
        except ValidationError as e:
            return Response(data={
                "errors": e.detail,
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(data={
            "message": "회원가입이 완료되었습니다.",
        }, status=status.HTTP_201_CREATED)

class PasswordChangeView(GenericAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)
    throttle_scope = 'dj_rest_auth'

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(data={
                "errors": e.detail,
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(data={
            "message": "비밀번호가 변경되었습니다.",
        }, status=status.HTTP_200_OK)

class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)
    throttle_scope = 'dj_rest_auth'

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(data={
                "errors": e.detail,
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(data={
            "message": "비밀번호 재설정 이메일이 발송되었습니다.",
        }, status=status.HTTP_200_OK)
