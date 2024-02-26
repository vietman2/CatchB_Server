from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

from region.models import Sigungu
from .models import Facility, FacilityInfo
from .serializers import (
    FacilitySimpleSerializer, FacilityCreateSerializer,
    FacilityInfoCreateSerializer
)

class FacilityViewSet(ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySimpleSerializer
    http_method_names = ["get", "post"]

    @extend_schema(summary="시설 목록 조회", tags=["시설"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="시설 등록 신청", tags=["시설"])
    def create(self, request, *args, **kwargs):
        try:
            sigungu = Sigungu.objects.get_sigungu_from_bcode(request.data['bcode'])

            data = request.POST.copy()
            data['region'] = sigungu.pk

            facility_serializer = FacilityCreateSerializer(data=data)
            facility_serializer.is_valid(raise_exception=True)

            facility = facility_serializer.save()
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
        except ObjectDoesNotExist:
            # ObjectDoesNotExist: sigungu does not exist
            # MultiValueDictKeyError: bcode does not exist
            # ValueError: invalid bcode: cannot convert to int
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "존재하지 않는 지역코드입니다."}
            )
        except MultiValueDictKeyError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "지역 코드를 입력해주세요."}
            )
        except ValueError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "올바른 지역 코드를 입력해주세요."}
            )

        return Response(
            status=status.HTTP_201_CREATED,
            data={"message": "시설 등록 신청이 완료되었습니다.", "uuid": facility.uuid}
        )

    def custom_error_message(self, e):
        if "num_mounds" in e.detail:
            return e.detail["num_mounds"][0]
        if "num_plates" in e.detail:
            return e.detail["num_plates"][0]
        if "sunday_close" in e.detail:
            return e.detail["sunday_close"][0]
        if "sunday_open" in e.detail:
            return e.detail["sunday_open"][0]
        if "saturday_close" in e.detail:
            return e.detail["saturday_close"][0]
        if "saturday_open" in e.detail:
            return e.detail["saturday_open"][0]
        if "weekday_close" in e.detail:
            return e.detail["weekday_close"][0]
        if "weekday_open" in e.detail:
            return e.detail["weekday_open"][0]
        if "intro" in e.detail:
            return e.detail["intro"][0]
        if "images" in e.detail:
            return "아카데미를 소개하는 이미지를 최소 1장 업로드 해주세요."

        return "시설 정보 입력에 실패했습니다."

    @action(detail=True, methods=["post"])
    @extend_schema(summary="시설 정보 입력", tags=["시설"])
    def info(self, request):
        facility = self.get_object()
        facility_info_serializer = FacilityInfoCreateSerializer(data=request.data)

        try:
            if FacilityInfo.objects.filter(facility=facility).exists():
                raise ValidationError("이미 등록된 시설 정보입니다.")
            facility_info_serializer.is_valid(raise_exception=True)

            facility_info_serializer.convenience(request.POST.getlist('convenience'))
            facility_info_serializer.equipment(request.POST.getlist('equipment'))
            facility_info_serializer.others(request.POST.getlist('others'))
            facility_info_serializer.custom_equipment(request.POST.getlist('custom'))
            facility_info_serializer.upload_images(request.FILES.getlist('images'), facility.uuid)

            facility_info_serializer.validated_data['facility'] = facility

            facility_info_serializer.save()
        except ValidationError as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": self.custom_error_message(e)}
            )

        return Response(
            status=status.HTTP_201_CREATED,
            data={"message": "시설 정보 입력이 완료되었습니다."}
        )
