from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema

from .models import LessonProduct
from .serializers import LessonProductSerializer, LessonProductListSerializer

class LessonProductViewSet(ModelViewSet):
    queryset = LessonProduct.objects.all()
    serializer_class = LessonProductSerializer
    http_method_names = ["get", "post", "patch", "delete"]

    @extend_schema(summary="레슨 상품 목록 조회", tags=["레슨"])
    def list(self, request, *args, **kwargs):
        # 그냥 조회하면, 전체 목록 조회
        # query_params로 coach_id를 받으면, 해당 코치가 등록한 레슨 상품 목록 조회
        # query_params로 가격을 받으면, 해당 가격 이하의 레슨 상품 목록 조회

        coach_id = request.query_params.get("coach_uuid")
        price = request.query_params.get("price")

        if coach_id:
            queryset = LessonProduct.objects.filter(main_coach=coach_id)
        elif price:
            queryset = LessonProduct.objects.filter(price__lte=price)
        else:
            queryset = LessonProduct.objects.all()

        serializer = LessonProductListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(summary="레슨 상품 상세 조회", tags=["레슨"])
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = LessonProductSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(summary="레슨 상품 등록", tags=["레슨"])
    def create(self, request, *args, **kwargs):
        serializer = LessonProductSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(data={"message": e.detail}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(summary="레슨 상품 수정", tags=["레슨"])
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = LessonProductSerializer(instance, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.validate_partial_update(request.data)
        except ValidationError as e:
            return Response(data={"message": e.detail}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(summary="레슨 상품 삭제", tags=["레슨"])
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        LessonProduct.objects.filter(id=instance.id).update(deleted=True)
        return Response(status=status.HTTP_204_NO_CONTENT)
