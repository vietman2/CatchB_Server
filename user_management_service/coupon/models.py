from django.db import models
from django.utils.translation import gettext_lazy as _

class CouponStatus(models.TextChoices):
    ACTIVE      = 'ACTIVE', "사용 가능"
    USED        = 'USED', "사용 완료"
    EXPIRED     = 'EXPIRED', "쿠폰 만료"

class Coupon(models.Model):
    user        = models.ForeignKey(
        'user.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='user_coupons'
    )
    coupon_type = models.ForeignKey(
        'coupon.CouponType',
        on_delete=models.SET_NULL,
        null=True,
        related_name='coupon_type'
    )
    issued_at   = models.DateTimeField(auto_now_add=True)
    status      = models.CharField(
        max_length=10,
        choices=CouponStatus.choices,
        default=CouponStatus.ACTIVE
    )
    valid_until = models.DateTimeField(null=True)

    class Meta:
        db_table = 'coupon'
        verbose_name = _('coupon')
        verbose_name_plural = _('coupons')

class CouponType(models.Model):
    coupon_name = models.CharField(max_length=100)
    coupon_description = models.CharField(max_length=100)
    #coupon_image = models.ImageField(upload_to='coupon_images')
    registered_at = models.DateTimeField(auto_now_add=True)
    valid_days = models.IntegerField()

    class Meta:
        db_table = 'coupon_type'
        verbose_name = _('coupon_type')
        verbose_name_plural = _('coupon_types')
