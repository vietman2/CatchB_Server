from django.db import models

class PointStatus(models.TextChoices):
    ACTIVE      = 'ACTIVE', "사용 가능"
    PARTIAL     = 'PARTIAL', "부분 사용"
    USED        = 'USED', "사용 완료"
    EXPIRED     = 'EXPIRED', "기한 만료"
