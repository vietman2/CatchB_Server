from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from .models import Coupon
from .serializers import CouponSerializer, CouponClassCreateSerializer
from user.permissions import IsNormalUser

class CouponViewSet(ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch"]

    @extend_schema(exclude=True)
    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @extend_schema(exclude=True)
    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @extend_schema(summary="쿠폰 조회", tags=["쿠폰"])
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = CouponSerializer(queryset, many=True)
        return Response(serializer.data)
    
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
