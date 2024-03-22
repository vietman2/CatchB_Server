from django.db import models
from django.core.validators import MinValueValidator as Min, MaxValueValidator as Max

from core.models import Provider, Image     ## pylint: disable=E0611
from region.models import Sigungu

class Facility(Provider):
    name        = models.CharField(max_length=20)
    phone       = models.CharField(max_length=13)
    reg_code    = models.CharField(unique=True, editable=False, max_length=12)

    ## 상세 정보: 시설 주소
    # 주소
    region              = models.ForeignKey(Sigungu, on_delete=models.PROTECT)
    road_address_part1  = models.CharField(max_length=30)
    road_address_part2  = models.CharField(max_length=30)
    building_name       = models.CharField(max_length=30)
    eng_address         = models.CharField(max_length=80)
    jibun_address       = models.CharField(max_length=50)
    zip_code            = models.CharField(max_length=5)

    # 좌표
    longitude           = models.DecimalField(max_digits=10, decimal_places=7)
    latitude            = models.DecimalField(max_digits=10, decimal_places=7)

    # 지도 이미지
    map_image           = models.ImageField(blank=True)

    ## 상세 정보: 시설 계좌 정보
    ## TODO: ADD BANK INFO

    is_complete     = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        db_table = "facility"

class FacilityInfo(models.Model):
    ## 시설 기본 소개
    facility    = models.ForeignKey("Facility", on_delete=models.CASCADE)
    intro       = models.TextField()

    ## 시설 정보1: 기본 영업 시간
    weekday_open    = models.TimeField()
    weekday_close   = models.TimeField()
    saturday_open   = models.TimeField()
    saturday_close  = models.TimeField()
    sunday_open     = models.TimeField()
    sunday_close    = models.TimeField()

    ## 시설 정보2: 편의시설
    wifi            = models.BooleanField(default=False)
    water           = models.BooleanField(default=False)
    free_parking    = models.BooleanField(default=False)
    paid_parking    = models.BooleanField(default=False)
    resting_area    = models.BooleanField(default=False)
    separate_toilet = models.BooleanField(default=False)
    air_conditioner = models.BooleanField(default=False)
    heating         = models.BooleanField(default=False)
    locker          = models.BooleanField(default=False)
    changing_room   = models.BooleanField(default=False)
    shower          = models.BooleanField(default=False)
    sauna           = models.BooleanField(default=False)
    no_smoking      = models.BooleanField(default=False)
    smoking_room    = models.BooleanField(default=False)
    kids_room       = models.BooleanField(default=False)
    no_kids         = models.BooleanField(default=False)
    vending_machine = models.BooleanField(default=False)
    proshop         = models.BooleanField(default=False)

    ## 시설 정보3: 구비 시설
    num_mounds          = models.PositiveIntegerField(validators=[Min(0), Max(5)])
    num_plates          = models.PositiveIntegerField(validators=[Min(0), Max(5)])
    wood_bats           = models.BooleanField(default=False)
    aluminium_bats      = models.BooleanField(default=False)
    gloves              = models.BooleanField(default=False)
    catcher_gear        = models.BooleanField(default=False)
    pitching_machine    = models.BooleanField(default=False)
    batting_tee         = models.BooleanField(default=False)
    helmets             = models.BooleanField(default=False)
    speed_gun           = models.BooleanField(default=False)
    video_analysis      = models.BooleanField(default=False)
    monitor             = models.BooleanField(default=False)
    speaker             = models.BooleanField(default=False)
    fitness             = models.BooleanField(default=False)
    ## 커스텀 array field
    #custom_equipment    = ArrayField(
    #    models.CharField(max_length=30),
    #    default=list
    #)

    ## 시설 정보4: 기타
    group_lesson    = models.BooleanField(default=False)
    private_lesson  = models.BooleanField(default=False)
    cleats_allowed  = models.BooleanField(default=False)
    outdoor         = models.BooleanField(default=False)
    pets_allowed    = models.BooleanField(default=False)
    wheelchair      = models.BooleanField(default=False)

    ## 공개 정보: 시설 이미지 (주소)
    #images          = ArrayField(
    #    models.ImageField(upload_to="facility_images")
    #)

    objects = models.Manager()

    class Meta:
        db_table = "facility_info"

class FacilityImage(Image):
    facility    = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="fac_images")

    cover       = models.BooleanField(default=False)

    objects     = models.Manager()

    class Meta:
        db_table = 'facility_image'
