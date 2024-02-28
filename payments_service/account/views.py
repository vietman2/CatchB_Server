from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import Bank
from .serializers import BankListSerializer

class BankViewSet(ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankListSerializer
    http_method_names = ["get"]

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
