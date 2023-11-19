from rest_framework import serializers

from .models import Facility, Address

class FacilitySimpleSerializer(serializers.ModelSerializer):
    """
        목록 조회용 시설 정보
    """ 
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
        depth = 1

class AddressSerializer(serializers.ModelSerializer):
    """
        주소 정보
    """ 
    class Meta:
        model = Address
        fields = [
            "road_address",
            "road_address_part1",
            "road_address_part2",
            "eng_address",
            "jibun_address",
            "zip_code",
            "sido",
            "sigungu",
            "longitude",
            "latitude",
        ]
