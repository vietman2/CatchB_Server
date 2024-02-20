from django.db import models

class Sido(models.Model):
    sido_code = models.PositiveBigIntegerField(primary_key=True, db_comment="시/도 코드")
    sido_name = models.CharField(max_length=20, db_comment="시/도 이름")

    objects = models.Manager()

    class Meta:
        db_table = "sido"
        verbose_name = "시/도"
        verbose_name_plural = "시/도"

class SigunguManager(models.Manager):
    def get_sigungu_from_bcode(self, bcode):
        ## leave the first 5 digits and replace the rest with 0s
        try:
            sigungu_code = int(bcode[:5] + "00000")
            sigungu = self.get(sigungu_code=sigungu_code)
        # 2 exceptions: cannot convert to int, or no sigungu found
        except (ValueError, self.model.DoesNotExist):
            raise self.model.DoesNotExist

        return sigungu

class Sigungu(models.Model):
    sigungu_code    = models.PositiveBigIntegerField(primary_key=True, db_comment="시/군/구 코드")
    sigungu_name    = models.CharField(max_length=20, db_comment="시/군/구 이름")
    sido            = models.ForeignKey("Sido", on_delete=models.CASCADE, db_comment="시/도 코드")

    objects = SigunguManager()

    class Meta:
        db_table = "sigungu"
        verbose_name = "시/군/구"
        verbose_name_plural = "시/군/구"
