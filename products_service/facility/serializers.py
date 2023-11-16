from rest_framework import serializers

from .models import Facility

class FacilitySimpleSerializer(serializers.ModelSerializer):
    ## 목록 조회용 시설 정보
    class Meta:
        model = Facility
        fields = [
            "name",
            "uuid",
            "image_urls",
            "hashtags",
            "description",
            "address",
            "phone",
        ]
