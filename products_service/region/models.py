from django.db import models

class Sido(models.Model):
    sido_code = models.PositiveBigIntegerField(primary_key=True, db_comment="시/도 코드")
    sido_name = models.CharField(max_length=20, db_comment="시/도 이름")

    objects = models.Manager()

    class Meta:
        db_table = "sido"
        verbose_name = "시/도"
        verbose_name_plural = "시/도"

class Sigungu(models.Model):
    sigungu_code = models.PositiveBigIntegerField(primary_key=True, db_comment="시/군/구 코드")
    sigungu_name = models.CharField(max_length=20, db_comment="시/군/구 이름")
    sido_code = models.ForeignKey("Sido", on_delete=models.CASCADE, db_comment="시/도 코드")

    objects = models.Manager()

    class Meta:
        db_table = "sigungu"
        verbose_name = "시/군/구"
        verbose_name_plural = "시/군/구"
