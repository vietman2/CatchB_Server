import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
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
    def create(self, request, *args, **kwargs):     ## pylint: disable=R0911
        def get_coordinates(address):
            naver_geocode_url = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode'
            headers = {
                'X-NCP-APIGW-API-KEY-ID': settings.NAVER_CLIENT_ID,
                'X-NCP-APIGW-API-KEY': settings.NAVER_CLIENT_SECRET,
                'Accept': 'application/json',
            }
            params = {
                'query': address,
            }

            try:
                response = requests.request(
                        method='GET',
                        url=naver_geocode_url,
                        headers=headers,
                        params=params,
                        timeout=10,
                    )

                lat = response.json()['addresses'][0]['y']
                lng = response.json()['addresses'][0]['x']
                jibun_address = response.json()['addresses'][0]['jibunAddress']
                english_address = response.json()['addresses'][0]['englishAddress']

                return lat, lng, jibun_address, english_address

            except requests.RequestException as e:
                return Response(
                    {'message': str(e)},
                    status=status.HTTP_502_BAD_GATEWAY,
                )

        def handle_error(e):
            print(e.detail)
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

        try:
            if request.data['road_address_part1'] == "" or request.data['road_address_part2'] == "":
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"message": "주소를 입력해주세요."}
                )

            query = request.data['road_address_part1']
            lat, lng, jibun_address, english_address = get_coordinates(query)

            sigungu = Sigungu.objects.get_sigungu_from_bcode(request.data['bcode'])

            data = request.data.copy()
            data['region'] = sigungu.pk
            data['latitude'] = lat
            data['longitude'] = lng
            data['jibun_address'] = jibun_address
            data['eng_address'] = english_address

            facility_serializer = FacilityCreateSerializer(data=data)
            facility_serializer.is_valid(raise_exception=True)

            facility = facility_serializer.save()
        except ValidationError as e:
            return handle_error(e)
        except (ObjectDoesNotExist, MultiValueDictKeyError, ValueError):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "올바른 지역 코드를 입력해주세요."}
            )
        return Response(
            status=status.HTTP_201_CREATED,
            data={"message": "시설 등록 신청이 완료되었습니다.", "uuid": facility.uuid}
        )

    @action(detail=True, methods=["post"])
    @extend_schema(summary="시설 정보 입력", tags=["시설"])
    def info(self, request):
        def custom_error_message(self, e):      ## pylint: disable=R0911
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
                data={"message": custom_error_message(e)}
            )

        return Response(
            status=status.HTTP_201_CREATED,
            data={"message": "시설 정보 입력이 완료되었습니다."}
        )
