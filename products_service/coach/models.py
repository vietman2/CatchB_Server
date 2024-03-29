from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import Provider, Image ## pylint: disable=E0611
from facility.models import Facility
from .enums import CareerChoices

class Coach(Provider):
    certification       = models.FileField(blank=True)
    facility            = models.ForeignKey(Facility, null=True, on_delete=models.SET_NULL)

    baseball_career     = models.IntegerField(choices=CareerChoices.choices)

    ## 상세 정보: 코치 계좌 정보
    ## TODO: ADD BANK INFO

    objects = models.Manager()

    class Meta:
        db_table = 'coach'
        unique_together = ['member_uuid', 'uuid']

class CoachInfo(models.Model):
    ## 코치 기본 소개
    coach       = models.OneToOneField(
        Coach,
        on_delete=models.CASCADE,
        related_name='coach_info'
    )
    intro       = models.TextField()

    ## 코치 정보1: 전문 파트
    pitching        = models.BooleanField(default=False)
    batting         = models.BooleanField(default=False)
    defense         = models.BooleanField(default=False)
    catching        = models.BooleanField(default=False)
    rehabilitation  = models.BooleanField(default=False)
    conditioning    = models.BooleanField(default=False)

    ## 코치 정보2: 레슨 레벨
    beginner1       = models.BooleanField(default=False)
    beginner2       = models.BooleanField(default=False)
    amateur         = models.BooleanField(default=False)
    veteran         = models.BooleanField(default=False)
    rookie          = models.BooleanField(default=False)
    elite           = models.BooleanField(default=False)

    ## 코치 정보3: 레슨 유형
    individual      = models.BooleanField(default=False)
    group           = models.BooleanField(default=False)
    team            = models.BooleanField(default=False)
    others          = models.BooleanField(default=False)

    ## 코치 정보3: 소개 이미지/영상
    images          = models.ManyToManyField('CoachImage', related_name='coach_info')

    ## 코치 정보4: 선호 지역
    regions         = models.ManyToManyField('region.Sigungu', related_name='coach_info')

    objects         = models.Manager()

    class Meta:
        db_table = 'coach_info'

class CoachImage(Image):
    coach       = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='coach_images')

    cover       = models.BooleanField(default=False)

    objects     = models.Manager()

    class Meta:
        db_table = 'coach_image'
