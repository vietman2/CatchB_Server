import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from user.models import CustomUser
from .enums import PointStatus

class PointsUseDetails(models.Model):
    user        = models.ForeignKey(
        'user.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='user_points_use'
    )
    title       = models.CharField(max_length=20, db_comment="포인트 사용 제목")
    description = models.CharField(max_length=100, db_comment="포인트 사용 설명")
    points      = models.IntegerField(default=0, db_comment="사용 포인트")
    used_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'points_use_details'
        verbose_name = _('points use details')
        verbose_name_plural = _('points use details')
        ordering = ['-used_at']
    
class PointsEarnDetails(models.Model):
    user        = models.ForeignKey(
        'user.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='user_points_earn'
    )
    title       = models.CharField(max_length=20, db_comment="포인트 적립 제목")
    description = models.CharField(max_length=100, db_comment="포인트 적립 설명")
    points      = models.IntegerField(default=0, db_comment="적립 포인트")
    earned_at   = models.DateTimeField(auto_now_add=True)
    valid_days  = models.IntegerField(default=0, db_comment="유효기간 (일수))")

    class Meta:
        db_table = 'points_earn_details'
        verbose_name = _('points earn details')
        verbose_name_plural = _('points earn details')
        ordering = ['-earned_at']

class PointsManager(models.Manager):
    def total_points(self, user_uuid):
        # user_uuid dne
        try:
            CustomUser.objects.get(uuid=user_uuid)
            # only active and partial points
            points = self.filter(
                user__uuid=user_uuid,
                status__in=[PointStatus.ACTIVE, PointStatus.PARTIAL]
            )
            total_points = 0
            for point in points:
                total_points += point.remaining_points

            return total_points
        except ValidationError as e:
            raise ValueError("유효한 user_uuid가 아닙니다.") from e

    def use_points(self, **kwargs):
        user_uuid = kwargs.get("user").uuid
        points_to_use = kwargs.get("points")
        # only active and partial points
        points = self.filter(
            user__uuid=user_uuid,
            status__in=[PointStatus.ACTIVE, PointStatus.PARTIAL]
        )

        # not enough points
        if self.total_points(user_uuid) < points_to_use:
            raise ValueError("not enough points.")

        # use points from least remaining valid_until
        # if remaining points are not enough, use all remaining points
        # and move on to next point
        points = points.order_by('valid_until')
        for point in points:
            if point.remaining_points == points_to_use:
                ## 해당 적립금을 모두 사용하고 끝
                point.status = PointStatus.USED
                point.used_points += points_to_use
                point.save()
                break
            elif point.remaining_points > points_to_use:
                ## 해당 적립금을 사용하고도 남음
                point.status = PointStatus.PARTIAL
                point.used_points += points_to_use
                point.save()
                break
            else:
                ## 해당 적립금을 모두 사용하고 다음 적립금으로 넘어감
                points_to_use -= point.remaining_points
                point.status = PointStatus.USED
                point.used_points += point.remaining_points
                point.save()
                continue

        PointsUseDetails.objects.create(
            user_id=user_uuid,
            title=kwargs.get("title"),
            description=kwargs.get("description"),
            points=kwargs.get("points")
        )

    def earn_points(self, **kwargs):
        user_uuid = kwargs.get("user").uuid
        PointsEarnDetails.objects.create(
            user_id=user_uuid,
            title=kwargs.get("title"),
            description=kwargs.get("description"),
            points=kwargs.get("points"),
            valid_days=kwargs.get("valid_days")
        )
        valid_until_raw = datetime.datetime.now() + datetime.timedelta(days=kwargs.get("valid_days"))
        valid_until = timezone.make_aware(valid_until_raw, timezone.get_current_timezone())

        self.create(
            user_id=user_uuid,
            points=kwargs.get("points"),
            valid_until=valid_until
        )

class UserPoints(models.Model):
    user        = models.ForeignKey(
        'user.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='user_points'
    )
    points      = models.IntegerField(db_comment="적립 포인트")
    used_points = models.IntegerField(default=0, db_comment="사용 포인트")
    created_at  = models.DateTimeField(auto_now_add=True)
    status      = models.CharField(
        max_length=10,
        choices=PointStatus.choices,
        default=PointStatus.ACTIVE
    )
    valid_until = models.DateTimeField()

    objects = PointsManager()

    @property
    def remaining_points(self):
        return self.points - self.used_points

    class Meta:
        db_table = 'points'
        verbose_name = _('points')
        verbose_name_plural = _('points')
        ordering = ['-created_at']
