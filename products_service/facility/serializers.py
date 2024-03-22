import re
from django.core.files.storage import default_storage
from rest_framework import serializers

from coach.models import Coach
from coach.serializers import CoachProfileSerializer
from region.models import Sigungu
from .models import Facility, FacilityInfo, FacilityImage, CustomEquipment

class FacilitySimpleSerializer(serializers.ModelSerializer):
    """
        목록 조회용 시설 정보
    """
    region  = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()

    class Meta:
        model = Facility
        fields = [
            "name",
            "uuid",
            "region",
            "profile",
            "latitude",
            "longitude",
        ]

    def get_region(self, obj):
        return Sigungu.objects.get_display_name(obj.region)

    def get_profile(self, obj):
        return obj.fac_images.filter(cover=True).first().image.url

class FacilityDetailSerializer(serializers.ModelSerializer):
    """
        상세 조회용 시설 정보
    """
    owner_name  = serializers.SerializerMethodField()
    owner_phone = serializers.SerializerMethodField()
    address     = serializers.SerializerMethodField()

    class Meta:
        model = Facility
        fields = [
            "name",
            "phone",
            "owner_name",
            "owner_phone",
            "address",
            "map_image",
        ]

    def get_owner_name(self, obj):
        return obj.member_name

    def get_owner_phone(self, obj):
        return obj.member_phone

    def get_address(self, obj):
        return f"{obj.road_address_part1} {obj.road_address_part2} ({obj.building_name})"

class FacilityImageSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField()

    class Meta:
        model = FacilityImage
        fields = [
            "uri",
        ]

    def get_uri(self, obj):
        return obj.image.url

class FacilityInfoDetailSerializer(serializers.ModelSerializer):
    facility = FacilityDetailSerializer()
    images = FacilityImageSerializer(many=True)
    coaches = serializers.SerializerMethodField()

    class Meta:
        model = FacilityInfo
        fields = [
            "intro",
            "facility",
            "images",
            "coaches",
        ]

    def get_coaches(self, obj):
        coaches = Coach.objects.filter(facility=obj.facility)
        serializer = CoachProfileSerializer(coaches, many=True)

        return serializer.data

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
            "member_uuid",
            "member_name",
            "member_phone",
            "name",
            "phone",
            "reg_code",
            "region",
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

        return facility

class FacilityInfoCreateSerializer(serializers.ModelSerializer):
    """
        시설 정보 수정용 시설 정보
    """
    intro = serializers.CharField(
        error_messages={
            "blank": "시설 소개글을 입력해주세요."
        }
    )
    weekday_open = serializers.TimeField(
        error_messages={
            "invalid": "평일 오픈 시간을 올바르게 입력해주세요."
        }
    )
    weekday_close = serializers.TimeField(
        error_messages={
            "invalid": "평일 마감 시간을 올바르게 입력해주세요."
        }
    )
    saturday_open = serializers.TimeField(
        error_messages={
            "invalid": "토요일 오픈 시간을 올바르게 입력해주세요."
        }
    )
    saturday_close = serializers.TimeField(
        error_messages={
            "invalid": "토요일 마감 시간을 올바르게 입력해주세요."
        }
    )
    sunday_open = serializers.TimeField(
        error_messages={
            "invalid": "일요일 오픈 시간을 올바르게 입력해주세요."
        }
    )
    sunday_close = serializers.TimeField(
        error_messages={
            "invalid": "일요일 마감 시간을 올바르게 입력해주세요."
        }
    )
    num_mounds = serializers.IntegerField(
        error_messages={
            "invalid": "마운드 수를 입력해주세요."
        }
    )
    num_plates = serializers.IntegerField(
        error_messages={
            "invalid": "타석 수를 입력해주세요."
        }
    )

    class Meta:
        model = FacilityInfo
        fields = [
            "intro",
            "weekday_open",
            "weekday_close",
            "saturday_open",
            "saturday_close",
            "sunday_open",
            "sunday_close",
            "num_mounds",
            "num_plates",
        ]

    def convenience(self, choices):     ## pylint: disable=R0912
        if 'Wi-Fi' in choices:
            self.validated_data['wifi'] = True
        if '정수기 / 냉온수기' in choices:
            self.validated_data['water'] = True
        if '주차가능 (무료)' in choices:
            self.validated_data['free_parking'] = True
        if '주차가능 (유료)' in choices:
            self.validated_data['paid_parking'] = True
        if '휴게공간' in choices:
            self.validated_data['resting_area'] = True
        if '남녀화장실 구분' in choices:
            self.validated_data['separate_toilet'] = True
        if '에어컨' in choices:
            self.validated_data['air_conditioner'] = True
        if '난방' in choices:
            self.validated_data['heating'] = True
        if '락커' in choices:
            self.validated_data['locker'] = True
        if '탈의실' in choices:
            self.validated_data['changing_room'] = True
        if '샤워실' in choices:
            self.validated_data['shower'] = True
        if '사우나' in choices:
            self.validated_data['sauna'] = True
        if '금연시설' in choices:
            self.validated_data['no_smoking'] = True
        if '흡연실' in choices:
            self.validated_data['smoking_room'] = True
        if '어린이 놀이시설' in choices:
            self.validated_data['kids_room'] = True
        if '노키즈존' in choices:
            self.validated_data['no_kids'] = True
        if '자판기' in choices:
            self.validated_data['vending_machine'] = True
        if '프로샵' in choices:
            self.validated_data['proshop'] = True

    def equipment(self, choices):
        if "나무배트" in choices:
            self.validated_data['wood_bats'] = True
        if "알루미늄배트" in choices:
            self.validated_data['aluminium_bats'] = True
        if "글러브 대여" in choices:
            self.validated_data['gloves'] = True
        if "포수장비 대여" in choices:
            self.validated_data['catcher_gear'] = True
        if "피칭머신" in choices:
            self.validated_data['pitching_machine'] = True
        if "배팅티" in choices:
            self.validated_data['batting_tee'] = True
        if "헬멧 대여" in choices:
            self.validated_data['helmets'] = True
        if "스피드건" in choices:
            self.validated_data['speed_gun'] = True
        if "영상분석" in choices:
            self.validated_data['video_analysis'] = True
        if "모니터" in choices:
            self.validated_data['monitor'] = True
        if "스피커" in choices:
            self.validated_data['speaker'] = True
        if "헬스기구" in choices:
            self.validated_data['fitness'] = True

    def others(self, choices):
        if "단체 수업 가능" in choices:
            self.validated_data['group_lesson'] = True
        if "개인 코치 영업 가능" in choices:
            self.validated_data['private_lesson'] = True
        if "스파이크 착용 가능" in choices:
            self.validated_data['cleats_allowed'] = True
        if "야외 시설" in choices:
            self.validated_data['outdoor'] = True
        if "반려동물 출입가능" in choices:
            self.validated_data['pets_allowed'] = True
        if "휠체어 출입가능" in choices:
            self.validated_data['wheelchair'] = True

    def custom_equipment(self, choices):
        custom = []
        for item in choices:
            equipment = CustomEquipment.objects.create(name=item)
            custom.append(equipment)

        self.validated_data['custom_equipment'] = custom

    def upload_images(self, data, uuid):
        images = []
        for image in data:
            # first image: image.obj.cover = True
            cover = False
            if not images:
                cover = True

            path = f"products/facility/{uuid}/{image.name}"
            default_storage.save(path, image)
            facility_image = FacilityImage.objects.create(
                facility=self.validated_data['facility'],
                image=path,
                cover=cover
            )
            images.append(facility_image)

        self.validated_data['images'] = images

    def save(self, **kwargs):
        custom_equipment = self.validated_data.pop('custom_equipment')
        images = self.validated_data.pop('images')
        facility_info = FacilityInfo.objects.create(**self.validated_data)
        facility_info.custom_equipment.set(custom_equipment)
        facility_info.images.set(images)

        return facility_info
