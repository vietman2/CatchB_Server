import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

from facility.models import Facility
from .enums import CareerChoices

class Coach(models.Model):
    coach_uuid          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_uuid           = models.UUIDField(editable=False)
    coach_name          = models.CharField(max_length=30)
    coach_phone         = models.CharField(max_length=20)
    certification       = models.FileField()
    facility            = models.ForeignKey(Facility, null=True, on_delete=models.SET_NULL)

    baseball_career     = models.IntegerField(choices=CareerChoices.choices)

    ## 상세 정보: 코치 계좌 정보
    ## TODO: ADD BANK INFO

    is_confirmed        = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        db_table = 'coach'

class CoachInfo(models.Model):
    ## 코치 기본 소개
    coach       = models.ForeignKey('Coach', on_delete=models.CASCADE)
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
    ## TODO: Add Later

    objects = models.Manager()

    class Meta:
        db_table = 'coach_info'
