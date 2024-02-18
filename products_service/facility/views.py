from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from drf_spectacular.utils import extend_schema

from region.models import Sigungu
from .models import Facility
from .serializers import FacilitySimpleSerializer, FacilityCreateSerializer

class FacilityViewSet(ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySimpleSerializer
    http_method_names = ["get", "post", "put", "delete"]

    @extend_schema(summary="시설 목록 조회", tags=["시설"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="시설 등록 신청", tags=["시설"])
    def create(self, request, *args, **kwargs):
        sigungu = Sigungu.objects.get_sigungu_from_bcode(request.data['bcode'])

        data = request.data
        data['region'] = sigungu.pk

        facility_serializer = FacilityCreateSerializer(data=data)

        try:
            facility_serializer.is_valid(raise_exception=True)

            facility_serializer.save()
        except ValidationError as e:
            if "name" in e.detail:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"message": e.detail["name"][0]}
                )
            if "phone" in e.detail:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"message": e.detail["phone"][0]}
                )
            if "reg_code" in e.detail:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"message": e.detail["reg_code"][0]}
                )

            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "시설 등록 신청에 실패했습니다."}
            )

        return Response(
            status=status.HTTP_201_CREATED,
            data={"message": "시설 등록 신청이 완료되었습니다."}
        )

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(exclude=True)
    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(exclude=True)
    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
