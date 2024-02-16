import random
import string
from django.db import models
from django.utils.translation import gettext_lazy as _

from .enums import CouponStatus, CouponIssuerType, CouponType

class Coupon(models.Model):
    user            = models.ForeignKey(
        'user.CustomUser',
        on_delete=models.PROTECT,
        related_name='user_coupons'
    )
    coupon_class    = models.ForeignKey(
        'coupon.CouponClass',
        on_delete=models.PROTECT,
        related_name='coupon_class'
    )
    issued_at       = models.DateTimeField()
    status          = models.CharField(
        max_length=3,
        choices=CouponStatus.choices,
        default=CouponStatus.ACTIVE
    )
    valid_until     = models.DateTimeField(null=True)
    used_at         = models.DateTimeField(null=True, default=None)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'coupon'
        verbose_name = _('coupon')
        verbose_name_plural = _('coupons')

class CouponClass(models.Model):
    def coupon_code_generator():    # pylint: disable=E0211
        # generate a random xxxx-xxxx-xxxx-xxxx coupon code
        def generate_part():
            return ''.join(random.choices(string.digits + string.ascii_uppercase, k=4))

        coupon_code = '-'.join([generate_part() for _ in range(4)])

        return coupon_code

    code                = models.CharField(
        max_length=19,
        primary_key=True,
        default=coupon_code_generator,
        editable=False
    )
    coupon_name         = models.CharField(max_length=100)
    coupon_description  = models.CharField(max_length=100)
    coupon_issuer_type  = models.CharField(
        max_length=3,
        choices=CouponIssuerType.choices,
        default=CouponIssuerType.NULL
    )
    coupon_issuer       = models.ForeignKey(
        'user.CustomUser',
        on_delete=models.PROTECT,
        related_name='coupon_issuer'
    )

    issue_valid_days    = models.IntegerField(default=365)
    use_valid_days      = models.IntegerField(default=365)
    registered_at       = models.DateTimeField(auto_now_add=True)

    max_count           = models.IntegerField()
    current_count       = models.IntegerField(default=0)
    multiple_use        = models.BooleanField(default=False)

    coupon_type         = models.CharField(
        max_length=4,
        choices=CouponType.choices,
        default=CouponType.PERCENTAGE
    )
    discount_value      = models.IntegerField()

    objects = models.Manager()

    class Meta:
        db_table = 'coupon_class'
        verbose_name = _('coupon class')
        verbose_name_plural = _('coupon classes')
