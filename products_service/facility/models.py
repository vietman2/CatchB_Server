import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField

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
    ## 시설 기본 소개
    facility    = models.ForeignKey("Facility", on_delete=models.CASCADE, db_comment="시설 고유번호")
    intro       = models.TextField(db_comment="시설 소개글")

    ## 시설 정보1: 기본 영업 시간
    weekday_open    = models.TimeField(db_comment="평일 오픈 시간")
    weekday_close   = models.TimeField(db_comment="평일 마감 시간")
    saturday_open   = models.TimeField(db_comment="토요일 오픈 시간")
    saturday_close  = models.TimeField(db_comment="토요일 마감 시간")
    sunday_open     = models.TimeField(db_comment="일요일 오픈 시간")
    sunday_close    = models.TimeField(db_comment="일요일 마감 시간")

    ## 시설 정보2: 편의시설
    wifi            = models.BooleanField(default=False, db_comment="와이파이")
    water           = models.BooleanField(default=False, db_comment="정수기")
    free_parking    = models.BooleanField(default=False, db_comment="무료 주차")
    paid_parking    = models.BooleanField(default=False, db_comment="유료 주차")
    resting_area    = models.BooleanField(default=False, db_comment="휴게공간")
    separate_toilet = models.BooleanField(default=False, db_comment="남녀 화장실 구분")
    air_conditioner = models.BooleanField(default=False, db_comment="에어컨")
    heating         = models.BooleanField(default=False, db_comment="난방")
    locker          = models.BooleanField(default=False, db_comment="사물함")
    changing_room   = models.BooleanField(default=False, db_comment="탈의실")
    shower          = models.BooleanField(default=False, db_comment="샤워")
    sauna           = models.BooleanField(default=False, db_comment="사우나")
    no_smoking      = models.BooleanField(default=False, db_comment="금연구역")
    smoking_room    = models.BooleanField(default=False, db_comment="흡연실")
    kids_room       = models.BooleanField(default=False, db_comment="키즈룸")
    no_kids         = models.BooleanField(default=False, db_comment="노키즈존")

    ## 시설 정보3: 구비 시설
    num_mounds       = models.PositiveIntegerField(db_comment="마운드 수")
    num_plates       = models.PositiveIntegerField(db_comment="타석 수")
    wood_bats        = models.BooleanField(default=False, db_comment="목재배트")
    aluminium_bats   = models.BooleanField(default=False, db_comment="알루미늄배트")
    glove            = models.BooleanField(default=False, db_comment="글러브")
    catcher_gear     = models.BooleanField(default=False, db_comment="캐쳐장비")
    pitching_machine = models.BooleanField(default=False, db_comment="피칭머신")
    batting_tee      = models.BooleanField(default=False, db_comment="배팅티")
    helmets          = models.BooleanField(default=False, db_comment="헬멧")
    speed_gun        = models.BooleanField(default=False, db_comment="스피드건")
    video_analysis   = models.BooleanField(default=False, db_comment="영상분석")
    monitor          = models.BooleanField(default=False, db_comment="모니터")
    speaker          = models.BooleanField(default=False, db_comment="스피커")
    fitness          = models.BooleanField(default=False, db_comment="피트니스")
    vending_machine  = models.BooleanField(default=False, db_comment="자판기")
    proshop          = models.BooleanField(default=False, db_comment="프로샵")
    ## 커스텀 array field

    ## 시설 정보4: 기타
    group_lesson    = models.BooleanField(default=False, db_comment="그룹레슨")
    private_lesson  = models.BooleanField(default=False, db_comment="개인레슨")
    cleats_allowed  = models.BooleanField(default=False, db_comment="스파이크 허용")
    outdoor         = models.BooleanField(default=False, db_comment="야외시설")
    pets_allowed    = models.BooleanField(default=False, db_comment="애완동물 허용")
    wheelchair      = models.BooleanField(default=False, db_comment="휠체어")

    ## 공개 정보: 시설 이미지 (주소)
    images      = ArrayField(models.ImageField(upload_to="facility_images"), db_comment="시설 이미지", blank=True, null=True)


    objects = models.Manager()

    class Meta:
        db_table = "facility_info"
        verbose_name = "시설 정보"
        verbose_name_plural = "시설 정보"
