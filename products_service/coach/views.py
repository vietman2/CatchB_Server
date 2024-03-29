from django.db.models import Q
from django.core.exceptions import ValidationError as DjValidError
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

from .enums import CareerChoices
from .models import Coach, CoachInfo
from .serializers import (
    CoachSimpleSerializer, CoachInfoDetailSerializer,
    CoachCreateSerializer, CoachInfoCreateSerializer
)

def get_career_choice(choice):
    for career in CareerChoices:
        if career.label == choice:
            return career.value

    return None

class CoachViewSet(ModelViewSet):
    queryset = Coach.objects.all()
    serializer_class = CoachSimpleSerializer
    http_method_names = ["get", "post"]

    @extend_schema(summary="코치 목록 조회", tags=["코치"])
    def list(self, request, *args, **kwargs):
        ## TODO: pagination, filter based on lat and lng
        queryset = self.queryset.filter(is_confirmed=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

    @extend_schema(summary="코치 상세 조회", tags=["코치"])
    def retrieve(self, request, *args, **kwargs):
        coach = self.get_object()
        instance = CoachInfo.objects.get(coach=coach)
        serializer = CoachInfoDetailSerializer(instance)
        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

    @extend_schema(summary="코치 목록 조회", tags=["코치"])
    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            data['baseball_career'] = get_career_choice(data['baseball_career'])
            serializer = CoachCreateSerializer(data=data)
            serializer.is_valid(raise_exception=True)

            coach = serializer.save()

            return Response(
                status=status.HTTP_201_CREATED,
                data={"uuid": coach.uuid}
            )

        except ValidationError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "잘못된 요청입니다."}
            )

    @action(detail=True, methods=["post"])
    @extend_schema(summary="코치 상세 조회", tags=["코치"])
    def info(self, request, *args, **kwargs):   ## pylint: disable=W0613
        coach = self.get_object()
        serializer = CoachInfoCreateSerializer(data=request.data)

        try:
            if CoachInfo.objects.filter(coach=coach).exists():
                raise ValidationError("이미 코치 정보가 입력되었습니다.")

            serializer.is_valid(raise_exception=True)
            serializer.specialty(request.POST.getlist("specialty"))
            serializer.level(request.POST.getlist("level"))
            serializer.lesson_type(request.POST.getlist("lesson_type"))

            serializer.validated_data["coach"] = coach
            serializer.upload_images(request.FILES.getlist("images"), coach.uuid)

            serializer.save()

            return Response(
                status=status.HTTP_201_CREATED,
                data={"message": "코치 정보 입력이 완료되었습니다."}
            )

        except ValidationError as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": e.detail[0]}
            )

    @action(detail=False, methods=["get"])
    @extend_schema(summary="코치 등록 현황 조회", tags=["코치"])
    def status(self, request, *args, **kwargs): ## pylint: disable=W0613
        try:
            user_uuid = request.query_params["uuid"]

            q = Q()
            q &= Q(member_uuid=user_uuid)

            coach = Coach.objects.filter(q)

            if not coach.exists():
                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        "step": 0,
                        "title": "등록 시작",
                        "message": "코치 등록을 시작해 보세요!"
                    }
                )

            coach = coach.first()

            if not CoachInfo.objects.filter(coach=coach).exists():
                step = 1
            #elif coach.bank is None:
            #    step = 2
            #elif coach.products.count() == 0:
            #    step = 3
            else:
                return Response(
                    status=status.HTTP_200_OK,
                    data={
                        "step": -1,
                        "title": "승인 대기",
                        "message": "코치 등록 절차가 완료되어 승인 대기중입니다."
                    }
                )

            return Response(
                status=status.HTTP_200_OK,
                data={
                    "coach": coach.uuid,
                    "step": step,
                    "status": coach.is_confirmed,
                    "title": "이어서 등록하기",
                    "message": "코치 등록이 진행중입니다.\n코치님에 대한 상세 정보를 입력해주세요."
                }
            )

        except (ValidationError, DjValidError, MultiValueDictKeyError):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "잘못된 요청입니다."}
            )
