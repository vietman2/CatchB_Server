from django.db import models

class ExperienceTierChoices(models.IntegerChoices):
    BEGINNER = 0, '초보'
    INTERMEDIATE = 1, '중급'
    ADVANCED = 2, '고급'

class RegisterRouteChoices(models.IntegerChoices):
    CATCHB = 0, '캐치비'
    KAKAO = 1, '카카오'
    NAVER = 2, '네이버'