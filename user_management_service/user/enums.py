from django.db import models

class ExperienceTierChoices(models.IntegerChoices):
    UNDEFINED = 0, '미입력'
    BEGINNER = 1, '초보'
    INTERMEDIATE = 2, '중급'
    ADVANCED = 3, '고급'

class RegisterRouteChoices(models.IntegerChoices):
    UNDEFINED = 0, '미입력'
    CATCHB = 1, '캐치비'
    KAKAO = 2, '카카오'
    NAVER = 3, '네이버'
