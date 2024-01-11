from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.serializers import ValidationError
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from user.models import CustomUser
from .models import UserPoints
from .serializers import (
    EarnPointsSerizlier,
    UsePointsSerializer, PointsDetailSerializer
)

class PointViewSet(ModelViewSet):
    queryset = UserPoints.objects.all()
    serializer_class = PointsDetailSerializer
    permission_classes = [IsAuthenticated,]
    http_method_names = ["get", "post", "patch"]

    @extend_schema(exclude=True)
    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @extend_schema(exclude=True)
    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(summary="포인트 적립", tags=["포인트"])
    def create(self, request, *args, **kwargs):
        ## TODO: FIX ME: Create EarnDetail Object
        serializer = EarnPointsSerizlier(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": e.detail}
            )

        serializer.save()

        return Response(
            status=status.HTTP_201_CREATED,
            data=serializer.data
        )

    @extend_schema(summary="포인트 사용 (차감)", tags=["포인트"])
    @action(
        detail=False,
        methods=["PATCH"],
        serializer_class=UsePointsSerializer
    )
    # pylint: disable=W0613
    def use(self, request, *args, **kwargs):
        ## TODO: FIX ME: Create UseDetail Object
        serializer = UsePointsSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": e.detail}
            )

        try:
            serializer.save()
        except ValueError as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": e.args[0]}
            )

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

    @extend_schema(summary="포인트 적립 내역 조회", tags=["포인트"])
    def list(self, request, *args, **kwargs):
        user_uuid = request.query_params.get("uuid")

        if not user_uuid:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "user_uuid를 입력해주세요."}
            )
        try:
            user = CustomUser.objects.get(uuid=user_uuid)
        except DjangoValidationError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "유효한 user_uuid가 아닙니다."}
            )

        points = UserPoints.objects.filter(user=user)

        serializer = PointsDetailSerializer(points, many=True)
        total_points = UserPoints.objects.total_points(user_uuid)

        return Response(
            status=status.HTTP_200_OK,
            data={
                "total": total_points,
                "details": serializer.data,
            }
        )
