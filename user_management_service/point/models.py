from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class PointStatus(models.TextChoices):
    ACTIVE      = 'ACTIVE', "사용 가능"
    PARTIAL     = 'PARTIAL', "부분 사용"
    USED        = 'USED', "사용 완료"
    EXPIRED     = 'EXPIRED', "기한 만료"

class PointsManager(models.Manager):
    def total_points(self, user_uuid):
        # user_uuid dne
        try:
            self.filter(user__uuid=user_uuid).exists()
        except ValidationError as e:
            raise ValueError("유효한 user_uuid가 아닙니다.") from e

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
            if point.remaining_points == points_to_use:
                point.status = PointStatus.USED
                point.used_points += points_to_use
                point.save()
                break
            if point.remaining_points > points_to_use:
                point.status = PointStatus.PARTIAL
                point.used_points += points_to_use
                point.save()
                break

            points_to_use -= point.remaining_points
            point.status = PointStatus.USED
            point.used_points += point.remaining_points
            point.save()
            continue

class Points(models.Model):
    user        = models.ForeignKey(
        'user.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='user_points'
    )
    title       = models.CharField(max_length=20, db_comment="포인트 제목")
    description = models.CharField(max_length=100, db_comment="포인트 설명")
    points      = models.IntegerField(default=0, db_comment="적립 포인트")
    used_points = models.IntegerField(default=0, db_comment="사용 포인트")
    created_at  = models.DateTimeField(auto_now_add=True)
    status      = models.CharField(
        max_length=10,
        choices=PointStatus.choices,
        default=PointStatus.ACTIVE
    )
    valid_until = models.DateTimeField(null=True)

    objects = PointsManager()

    @property
    def remaining_points(self):
        return self.points - self.used_points

    class Meta:
        db_table = 'points'
        verbose_name = _('points')
        verbose_name_plural = _('points')
        ordering = ['-created_at']

class PointsUse(models.Model):
    pass
