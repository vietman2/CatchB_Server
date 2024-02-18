import re
from rest_framework import serializers

from .models import Facility, FacilityInfo

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
    name = serializers.CharField(
        error_messages={
            "blank": "시설 이름을 입력해주세요."
        }
    )
    phone = serializers.CharField(
        error_messages={
            "blank": "시설 전화번호를 입력해주세요."
        }
    )
    reg_code = serializers.CharField(
        error_messages={
            "blank": "사업자 등록번호를 입력해주세요.",
        }
    )

    class Meta:
        model = Facility
        fields = [
            "name",
            "owner_uuid",
            "owner_name",
            "owner_phone",
            "reg_code",
            "region",
            "phone",
            "road_address_part1",
            "road_address_part2",
            "building_name",
            "eng_address",
            "jibun_address",
            "zip_code",
            "latitude",
            "longitude",
        ]

    def validate_reg_code(self, value):
        ## 사업자 등록번호 중복 확인
        if Facility.objects.filter(reg_code=value).exists():
            raise serializers.ValidationError("이미 등록된 사업자 등록번호입니다.")
        ## 사업자 등록번호 형식 확인 (xxx-xx-xxxxx)
        if not re.match(r"^\d{3}-\d{2}-\d{5}$", value):
            raise serializers.ValidationError("올바른 사업자 등록번호 형식이 아닙니다.")

        return value

    def save(self, **kwargs):
        facility = Facility.objects.create(
            **self.validated_data
        )
        FacilityInfo.objects.create(
            facility=facility,
            intro="",
            description="",
        )
        return facility
