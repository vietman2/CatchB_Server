from django.db import models

class Facility(models.Model):
    name = models.CharField(max_length=100, db_comment="Facility Name. 시설 이름")
    address = models.CharField(max_length=255, db_comment="Facility Address. 시설 주소")
    phone = models.CharField(max_length=20, db_comment="Facility Phone Number. 시설 전화번호")

    ## 추후 추가할 필드
    ## 위치 좌표
    ## 간단한 설명
    ## 해시태그
    ## 코치진
    ## 기타

    class Meta:
        db_table = "facility"
