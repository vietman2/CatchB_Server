from rest_framework import serializers

from .models import Facility, Address, FacilityInfo

class FacilitySimpleSerializer(serializers.ModelSerializer):
    """
        목록 조회용 시설 정보
    """
    class Meta:
        model = Facility
        fields = [
            "name",
            "uuid",
            "address",
            "phone",
        ]
        depth = 1

class FacilityCreateSerializer(serializers.ModelSerializer):
    """
        시설 생성용 시설 정보
    """
    road_address = serializers.SerializerMethodField(read_only=True)
    road_address_part1 = serializers.SerializerMethodField(read_only=True)
    road_address_part2 = serializers.SerializerMethodField(read_only=True)
    eng_address = serializers.SerializerMethodField(read_only=True)
    jibun_address = serializers.SerializerMethodField(read_only=True)
    zip_code = serializers.SerializerMethodField(read_only=True)
    sido = serializers.SerializerMethodField(read_only=True)
    sigungu = serializers.SerializerMethodField(read_only=True)
    latitude = serializers.SerializerMethodField(read_only=True)
    longitude = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Facility
        fields = [
            "name",
            "owner_uuid",
            "owner_name",
            "owner_phone",
            "phone",
            "reg_code",
            "road_address",
            "road_address_part1",
            "road_address_part2",
            "eng_address",
            "jibun_address",
            "zip_code",
            "sido",
            "sigungu",
            "latitude",
            "longitude",
        ]

    def save(self, address=None, **kwargs):
        facility = Facility.objects.create(
            name=self.validated_data["name"],
            owner_uuid=self.validated_data["owner_uuid"],
            owner_name=self.validated_data["owner_name"],
            owner_phone=self.validated_data["owner_phone"],
            phone=self.validated_data["phone"],
            reg_code=self.validated_data["reg_code"],
            address=address,
        )
        FacilityInfo.objects.create(
            facility=facility,
            image_urls=[],
            hashtags=[],
            coaches=[],
            intro="",
            description="",
        )
        return facility

class AddressSerializer(serializers.ModelSerializer):
    """
        주소 정보
    """
    class Meta:
        model = Address
        fields = "__all__"

    def save(self, **kwargs):
        return Address.objects.create(**self.validated_data)
