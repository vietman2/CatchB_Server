from django.db import models
from django.utils.translation import gettext_lazy as _

class CouponStatus(models.TextChoices):
    ACTIVE      = 'ACTIVE', "사용 가능"
    USED        = 'USED', "사용 완료"
    EXPIRED     = 'EXPIRED', "기한 만료"

class CouponType(models.TextChoices):
    PERCENTAGE  = 'PERCENTAGE', "비율 할인"
    AMOUNT      = 'AMOUNT', "금액 할인"

class Coupon(models.Model):
    user            = models.ForeignKey(
        'user.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='user_coupons'
    )
    coupon_class    = models.ForeignKey(
        'coupon.CouponClass',
        on_delete=models.SET_NULL,
        null=True,
        related_name='coupon_class'
    )
    coupon_type     = models.CharField(
        max_length=10,
        choices=CouponType.choices,
        default=CouponType.PERCENTAGE
    )
    issued_at       = models.DateTimeField(auto_now_add=True)
    status          = models.CharField(
        max_length=10,
        choices=CouponStatus.choices,
        default=CouponStatus.ACTIVE
    )
    valid_until     = models.DateTimeField(null=True)

    class Meta:
        db_table = 'coupon'
        verbose_name = _('coupon')
        verbose_name_plural = _('coupons')

class CouponClass(models.Model):
    coupon_name         = models.CharField(max_length=100)
    coupon_description  = models.CharField(max_length=100)
    #coupon_image       = models.ImageField(upload_to='coupon_images')
    registered_at       = models.DateTimeField(auto_now_add=True)
    valid_days          = models.IntegerField()

    class Meta:
        db_table = 'coupon_class'
        verbose_name = _('coupon_class')
        verbose_name_plural = _('coupon_classes')
