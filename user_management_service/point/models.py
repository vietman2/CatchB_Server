import datetime
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from user.models import CustomUser
from .enums import PointStatus

class PointsUseDetails(models.Model):
    user        = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='user_points_use'
    )
    title       = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    points      = models.IntegerField(default=0)
    used_at     = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        db_table = 'points_use_details'
        ordering = ['-used_at']

class PointsEarnDetails(models.Model):
    user        = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='user_points_earn'
    )
    title       = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    points      = models.IntegerField(default=0)
    earned_at   = models.DateTimeField(auto_now_add=True)
    valid_days  = models.IntegerField(default=0)

    objects = models.Manager()

    class Meta:
        db_table = 'points_earn_details'
        ordering = ['-earned_at']

class PointsManager(models.Manager):
    def total_points(self, user_uuid):
        # user_uuid dne
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
            if point.remaining_points == points_to_use: # pylint: disable=R1723
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

        details = PointsUseDetails.objects.create(
            user_id=user_uuid,
            title=kwargs.get("title"),
            description=kwargs.get("description"),
            points=kwargs.get("points")
        )

        return details

    def earn_points(self, **kwargs):
        user_uuid = kwargs.get("user").uuid
        valid_days = kwargs.get("valid_days")
        PointsEarnDetails.objects.create(
            user_id=user_uuid,
            title=kwargs.get("title"),
            description=kwargs.get("description"),
            points=kwargs.get("points"),
            valid_days=kwargs.get("valid_days")
        )
        valid_until_raw = datetime.datetime.now() + datetime.timedelta(days=valid_days)
        valid_until = timezone.make_aware(valid_until_raw, timezone.get_current_timezone())

        obj = self.create(
            user_id=user_uuid,
            points=kwargs.get("points"),
            valid_until=valid_until
        )

        return obj

class UserPoints(models.Model):
    user        = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='user_points'
    )
    points      = models.IntegerField()
    used_points = models.IntegerField(default=0)
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
        ordering = ['-created_at']
