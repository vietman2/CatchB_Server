from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.exceptions import ValidationError

from .serializers import UserRegisterSerializer

class RegisterAPIView(CreateAPIView):
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

        super().post(request, *args, **kwargs)
        return Response(data={
            "message": "회원가입이 완료되었습니다.",
        }, status=status.HTTP_201_CREATED)
