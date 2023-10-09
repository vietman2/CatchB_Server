from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from django.core.exceptions import ValidationError

from .serializers import UserRegisterSerializer

class RegisterAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            super().post(request, *args, **kwargs)
            return Response(data={
                "message": "회원가입이 완료되었습니다.",
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(data={
                "errors": e.detail,
            }, status=status.HTTP_400_BAD_REQUEST)
