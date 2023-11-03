from django.db import models

class Coupon(models.Model):
    coupon_id = models.AutoField(primary_key=True)
    coupon_name = models.CharField(max_length=100)
    coupon_description = models.CharField(max_length=100)
    coupon_image = models.ImageField(upload_to='coupon_images')
    coupon_code = models.CharField(max_length=100)
    coupon_discount = models.FloatField()
    coupon_start_date = models.DateTimeField()
    coupon_end_date = models.DateTimeField()
    coupon_created_date = models.DateTimeField(auto_now_add=True)
    coupon_updated_date = models.DateTimeField(auto_now=True)
    coupon_is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.coupon_name
