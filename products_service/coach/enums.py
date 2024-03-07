from django.db import models

class CareerChoices(models.IntegerChoices):
    PROFESSIONAL    = 1, '프로 선수 출신'
    UNIVERSITY      = 2, '대학교 선수 출신'
    HIGH_SCHOOL     = 3, '고등학교 선수 출신'
    NON_ELITE       = 4, '비선수 출신'
    OTHERS          = 5, '기타'
