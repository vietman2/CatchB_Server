import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError as DjValidError
from django.core.files.base import ContentFile
from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import APIException
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

from region.models import Sigungu
from .models import Facility, FacilityInfo
from .serializers import (
    FacilitySimpleSerializer, FacilityCreateSerializer,
    FacilityInfoCreateSerializer, FacilityDetailSeralizer
)

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
        raise APIException(str(e))

def get_error_message(e):
    err_types = ["name", "phone", "reg_code", "num_mounds", "num_plates",
                 "sunday_close", "sunday_open", "saturday_close", "saturday_open",
                 "weekday_close", "weekday_open", "intro"]

    for err_type in err_types:
        if err_type in e.detail:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": e.detail[err_type][0]}
            )

    if "images" in e.detail:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={"message": "아카데미를 소개하는 이미지를 최소 1장 업로드 해주세요."}
        )

    return Response(
        status=status.HTTP_400_BAD_REQUEST,
        data={"message": "등록 실패했습니다."}
    )

def fetch_map_image(lat, lng):
    naver_staticmap_url = 'https://naveropenapi.apigw.ntruss.com/map-static/v2/raster'
    headers = {
        'X-NCP-APIGW-API-KEY-ID': settings.NAVER_CLIENT_ID,
        'X-NCP-APIGW-API-KEY': settings.NAVER_CLIENT_SECRET,
    }
    params = {
        'center': f'{lng},{lat}',
        'level': 15,
        'w': 500,
        'h': 300,
        'format': 'png',
        'markers': f'type:d|size:small|pos:{lng} {lat}|color:0x14863e|viewSizeRatio:0.75',
    }

    try:
        response = requests.request(
                method='GET',
                url=naver_staticmap_url,
                headers=headers,
                params=params,
                timeout=10,
            )

        return ContentFile(response.content)

    except requests.RequestException as e:
        raise APIException(str(e))

class FacilityViewSet(ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySimpleSerializer
    http_method_names = ["get", "post"]

    @extend_schema(summary="시설 상세 조회", tags=["시설"])
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = FacilityDetailSeralizer(instance)
        return Response(serializer.data)

    @extend_schema(summary="시설 목록 조회", tags=["시설"])
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        ## TODO: Facility.objects.get(is_confirmed=True)
        ## TODO: pagination, filter based on lat and lng
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(summary="시설 등록 신청", tags=["시설"])
    def create(self, request, *args, **kwargs):     ## pylint: disable=R0914, W0613
        try:
            query = request.data['road_address_part1']
            lat, lng, jibun_address, english_address = get_coordinates(query)

            sigungu = Sigungu.objects.get_sigungu_from_bcode(request.data['bcode'])

            data = request.data.copy()
            data['region'] = sigungu.pk
            data['latitude'] = lat
            data['longitude'] = lng
            data['jibun_address'] = jibun_address
            data['eng_address'] = english_address

            serializer = FacilityCreateSerializer(data=data)
            serializer.is_valid(raise_exception=True)

            facility = serializer.save()

            image = fetch_map_image(facility.latitude, facility.longitude)
            path = f"products/facility/{facility.uuid}/map_image.png"
            facility.map_image.save(path, image)

        except ValidationError as e:
            return get_error_message(e)
        except (ObjectDoesNotExist, MultiValueDictKeyError, ValueError):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "올바른 주소를 입력해주세요."}
            )
        except APIException as e:
            return Response(
                status=status.HTTP_502_BAD_GATEWAY,
                data={"message": str(e)}
            )
        return Response(
            status=status.HTTP_201_CREATED,
            data={"message": "시설 등록 신청이 완료되었습니다.", "uuid": facility.uuid}
        )

    @action(detail=True, methods=["post"])
    @extend_schema(summary="시설 정보 입력", tags=["시설"])
    def info(self, request, *args, **kwargs):       ## pylint: disable=W0613
        facility = self.get_object()
        serializer = FacilityInfoCreateSerializer(data=request.data)

        try:
            if FacilityInfo.objects.filter(facility=facility).exists():
                raise ValidationError("이미 등록된 시설 정보입니다.")

            serializer.is_valid(raise_exception=True)

            serializer.convenience(request.POST.getlist('convenience'))
            serializer.equipment(request.POST.getlist('equipment'))
            serializer.others(request.POST.getlist('others'))
            #serializer.custom_equipment(request.POST.getlist('custom'))
            #serializer.upload_images(request.FILES.getlist('images'), facility.uuid)

            serializer.validated_data['facility'] = facility

            serializer.save()

            return Response(
                status=status.HTTP_201_CREATED,
                data={"message": "시설 정보 입력이 완료되었습니다."}
            )

        except ValidationError as e:
            return get_error_message(e)

    @action(detail=False, methods=["get"])
    @extend_schema(summary="시설 등록 현황 조회", tags=["시설"])
    def status(self, request, *args, **kwargs):
        try:
            user_uuid = request.query_params["uuid"]

            q = Q()
            q &= Q(member_uuid=user_uuid)

            facilities = Facility.objects.filter(q)

            ## 0. 등록한 시설이 없음
            if not facilities.exists():
                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        "step": 0,
                        "title": "등록 시작",
                        "message": "사장님의 첫번째 아카데미를 등록해 보세요!"
                    }
                )

            q &= Q(is_complete=False)
            ## 1. if 등록 절차가 안끝난 아카데미가 없는 경우: 새로운 아카데미 등록
            if not facilities.filter(q).exists():
                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        "step": 0,
                        "title": "새로 등록하기",
                        "message": "이미 운영중인 아카데미가 있습니다.\n새로운 아카데미를 등록하시겠습니까?"
                    }
                )

            ## 2. if 시설 정보 입력이 안끝난 경우: step 1
            facility = facilities.filter(q).first()
            if not FacilityInfo.objects.filter(facility=facility).exists():
                step = 1
            ## TODO: Finish this
            #elif facility.bank is None:
            #    step = 2
            #elif facility.products.count() == 0:
            #    step = 3
            else:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"message": "오류가 발생했습니다. 나중에 다시 시도해주세요."}
                )

            return Response(
                status=status.HTTP_200_OK,
                data={
                    "facility": facility.uuid,
                    "step": step,
                    "status": facility.is_confirmed,
                    "title": "이어서 등록하기",
                    "message": "이미 등록중인 아카데미가 있습니다.\n아카데미 정보를 이어서 입력해주세요."
                }
            )

        except (ValidationError, DjValidError, MultiValueDictKeyError):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "잘못된 요청입니다."}
            )
