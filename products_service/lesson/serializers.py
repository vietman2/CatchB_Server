from rest_framework import serializers

from .models import LessonProduct

class LessonProductSerializer(serializers.ModelSerializer):
    """
        레슨 상품 정보
    """
    class Meta:
        model = LessonProduct
        fields = [
            "id",
            "title",
            "description",
            "price",
            "main_coach",
            "num_sessions",
        ]

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("가격은 0 이상이어야 합니다.")
        return value

    def validate_partial_update(self, data):
        if data == {}:
            raise serializers.ValidationError("수정할 필드를 입력해주세요.")
        return data

class LessonProductListSerializer(serializers.ModelSerializer):
    """
        레슨 목록 조회용 시리얼라이저
    """
    class Meta:
        model = LessonProduct
        fields = [
            "id",
            "title",
            "price",
            "main_coach",
            "num_sessions",
        ]
