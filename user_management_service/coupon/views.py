import datetime
from django.utils import timezone
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from celery.result import AsyncResult

from user.permissions import IsNormalUser
from .models import Coupon, CouponClass
from .serializers import CouponSerializer, CouponClassCreateSerializer
from .tasks import process_register
from .enums import CouponStatus

class CouponViewSet(ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch"]

    @extend_schema(exclude=True)
    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(exclude=True)
    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(summary="쿠폰 리스트 조회", tags=["쿠폰"])
    def list(self, request, *args, **kwargs):
        # return coupons that the user has
        coupons = Coupon.objects.filter(user=request.user, status=CouponStatus.ACTIVE)
        serializer = CouponSerializer(coupons, many=True)

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data
        )

    @extend_schema(summary="쿠폰 생성", tags=["쿠폰"])
    def create(self, request, *args, **kwargs):
        if IsNormalUser().has_permission(request, self):
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"message": "권한이 없습니다. 쿠폰 생성은 시설 관리자와 코치만 가능합니다."}
            )

        serializer = CouponClassCreateSerializer(data=request.data)

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
            data={"message": "쿠폰이 생성되었습니다."}
        )

    @extend_schema(summary="쿠폰 등록", tags=["쿠폰"])
    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def register(self, request, *args, **kwargs):
        coupon_code = request.data.get("coupon_code", None)
        now = datetime.datetime.now()
        request_datetime = timezone.make_aware(now, timezone.get_current_timezone())

        if not coupon_code:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "쿠폰 코드를 입력해주세요."}
            )

        try:
            coupon = CouponClass.objects.get(code=coupon_code)

            task = process_register.delay(
                request.user.pk,
                coupon.code,
                request_datetime
            )

            return Response(
                status=status.HTTP_202_ACCEPTED,
                data={"message": "일단 오케이.", "task_id": task.id}
            )
        except CouponClass.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": "존재하지 않는 쿠폰번호입니다."}
            )

    @extend_schema(summary="쿠폰 상태 확인", tags=["쿠폰"])
    @action(detail=False, methods=["get"], url_path="status", permission_classes=[IsAuthenticated])
    def check_status(self, request, *args, **kwargs):
        task_id = request.query_params.get("task_id", None)
        if not task_id:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "task_id를 입력해주세요."}
            )

        task_result = AsyncResult(task_id)

        if task_result.ready():
            return Response(
                status=status.HTTP_200_OK,
                data={"message": "쿠폰이 생성되었습니다."}
            )
        else:
            return Response(
                status=status.HTTP_202_ACCEPTED,
                data={"message": "쿠폰 생성 중입니다."}
            )
