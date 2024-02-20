from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema

from .models import Sido, Sigungu
from .serializers import SidoSerializer, SigunguSerializer

class RegionViewSet(ModelViewSet):
    queryset = Sido.objects.all()
    serializer_class = SidoSerializer
    http_method_names = ["get"]

    @extend_schema(summary="시도 목록 조회", tags=["지역"])
    def list(self, request, *args, **kwargs):
        sido_list = Sido.objects.all()
        sido_serializer = SidoSerializer(sido_list, many=True)

        sigungu_list = Sigungu.objects.all()
        sigungu_serializer = SigunguSerializer(sigungu_list, many=True)

        sigungu_by_sido = {}

        for sigungu in sigungu_list:
            sido_name = sigungu.sido.sido_name
            if sido_name not in sigungu_by_sido:
                sigungu_by_sido[sido_name] = []
            sigungu_by_sido[sido_name].append(sigungu.sigungu_name)

        return Response(
            status=status.HTTP_200_OK,
            data={
                "sido": sido_serializer.data,
                "sigungu": sigungu_serializer.data,
                "sigungu_by_sido": sigungu_by_sido,
            }
        )

    @extend_schema(exclude=True)
    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
