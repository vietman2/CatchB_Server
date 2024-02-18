import uuid
from django.db import models
#from django.contrib.postgres.fields import ArrayField

from region.models import Sigungu

class Facility(models.Model):
    ## 기본 정보: 시설 이름, 시설 고유번호, 시설 소유자 고유번호
    uuid        = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_comment="시설 고유번호"
    )
    name        = models.CharField(max_length=30, db_comment="시설 이름")
    owner_uuid  = models.UUIDField(db_comment="시설 소유자 유저번호")
    owner_name  = models.CharField(max_length=30, db_comment="시설 소유자 이름")
    owner_phone = models.CharField(max_length=20, db_comment="시설 소유자 전화번호")
    reg_code    = models.CharField(unique=True, max_length=20, db_comment="시설 사업자 등록번호")

    ## 상세 정보: 시설 지역, 시설 전화번호
    region      = models.ForeignKey(Sigungu, on_delete=models.PROTECT, db_comment="시설 시군구")
    phone       = models.CharField(max_length=20, db_comment="시설 전화번호")

    ## 상세 정보: 시설 주소
    # 주소
    road_address_part1  = models.CharField(max_length=255, db_comment="도로명 주소 (행정구역)")
    road_address_part2  = models.CharField(max_length=255, db_comment="도로명 주소 (상세영역)")
    building_name       = models.CharField(max_length=255, db_comment="건물 이름")
    eng_address         = models.CharField(max_length=255, db_comment="영문 주소")
    jibun_address       = models.CharField(max_length=255, db_comment="지번 주소")
    zip_code            = models.CharField(max_length=10, db_comment="우편번호")

    # 좌표
    longitude           = models.FloatField(db_comment="Longitude. 경도")
    latitude            = models.FloatField(db_comment="Latitude. 위도")

    is_confirmed = models.BooleanField(default=False, db_comment="시설 승인 여부")

    objects = models.Manager()

    class Meta:
        db_table = "facility"
        verbose_name = "시설"
        verbose_name_plural = "시설"

class FacilityInfo(models.Model):
    # 시설 정보
    facility = models.ForeignKey("Facility", on_delete=models.CASCADE, db_comment="시설 고유번호")

    ## 공개 정보: 시설 이미지 (주소), 시설 해시태그, 시설 코치 고유번호 JSON
    #image_urls  = ArrayField(models.CharField(max_length=255), db_comment="시설 이미지 URL")
    #hashtags    = ArrayField(models.CharField(max_length=255), db_comment="시설 해시태그")
    #coaches     = ArrayField(models.UUIDField(), db_comment="시설 코치 고유번호 배열")

    intro       = models.TextField(db_comment="시설 소개글")
    description = models.TextField(db_comment="시설 설명")

    objects = models.Manager()

    class Meta:
        db_table = "facility_info"
        verbose_name = "시설 정보"
        verbose_name_plural = "시설 정보"
