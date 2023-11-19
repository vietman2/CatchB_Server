from rest_framework import serializers

from .models import LessonProduct

class LessonProductSerializer(serializers.ModelSerializer):
    """
        레슨 상품 정보
    """ 
    class Meta:
        model = LessonProduct
        fields = [
            "title",
            "description",
            "price",
            "main_coach",
            "num_sessions",
            "num_finished",
            "num_booked",
        ]
