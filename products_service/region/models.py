from django.db import models

class Sido(models.Model):
    sido_code = models.PositiveBigIntegerField(primary_key=True)
    sido_name = models.CharField(max_length=20)
    label     = models.CharField(max_length=2)
    display   = models.CharField(max_length=4)

    objects = models.Manager()

    class Meta:
        db_table = "sido"

class SigunguManager(models.Manager):
    def get_sigungu_from_bcode(self, bcode):
        ## leave the first 5 digits and replace the rest with 0s
        sigungu_code = int(bcode[:5] + "00000")
        sigungu = self.get(sigungu_code=sigungu_code)

        return sigungu
    
    def get_display_name(self, obj):
        sido = obj.sido.label
        return f"{sido} {obj.sigungu_name}"

class Sigungu(models.Model):
    sigungu_code    = models.PositiveBigIntegerField(primary_key=True)
    sigungu_name    = models.CharField(max_length=20)
    sido            = models.ForeignKey("Sido", on_delete=models.CASCADE)

    objects = SigunguManager()

    class Meta:
        db_table = "sigungu"
