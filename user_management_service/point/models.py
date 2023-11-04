from django.db import models
from django.utils.translation import gettext_lazy as _

class PointStatus(models.TextChoices):
    ACTIVE      = 'ACTIVE', "사용 가능"
    USED        = 'USED', "사용 완료"
    EXPIRED     = 'EXPIRED', "쿠폰 만료"

class Points(models.Model):
    user        = models.ForeignKey(
        'user.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='user_points'
    )
    point       = models.IntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)
    status      = models.CharField(
        max_length=10,
        choices=PointStatus.choices,
        default=PointStatus.ACTIVE
    )
    valid_until = models.DateTimeField(null=True)

    class Meta:
        db_table = 'points'
        verbose_name = _('points')
        verbose_name_plural = _('points')
