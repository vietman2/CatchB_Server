from django.db import models

class Stars(models.IntegerChoices):
    ONE     = 1, "1"
    TWO     = 2, "2"
    THREE   = 3, "3"
    FOUR    = 4, "4"
    FIVE    = 5, "5"

class CoachReview(models.Model):
    coach       = models.UUIDField(null=False, blank=False, db_comment="코치 고유번호")
    user        = models.UUIDField(null=False, blank=False, db_comment="사용자 고유번호")
    content     = models.TextField(null=False, blank=False, db_comment="내용")
    content_open= models.BooleanField(default=False, db_comment="내용 공개 여부")
    images      = models.JSONField(null=True, blank=True, db_comment="이미지 URL 배열")
    stars       = models.IntegerField(
        choices=Stars.choices,
        db_comment="별점",
        null=False,
        blank=False
    )

    objects = models.Manager()

    class Meta:
        db_table = "coach_review"
        indexes = [
            models.Index(fields=["coach"], name="coach_review_coach_index"),
            models.Index(fields=["user"], name="coach_review_user_index"),
        ]
        verbose_name = "레슨 리뷰"
        verbose_name_plural = "레슨 리뷰"

class CoachLike(models.Model):
    coach      = models.UUIDField(null=False, blank=False, db_comment="코치 고유번호")
    user        = models.UUIDField(null=False, blank=False, db_comment="사용자 고유번호")

    class Meta:
        db_table = "coach_like"
        indexes = [
            models.Index(fields=["coach"], name="coach_like_coach_index"),
            models.Index(fields=["user"], name="coach_like_user_index"),
        ]
        verbose_name = "코치 좋아요"
        verbose_name_plural = "코치 좋아요"

class FacilityReview(models.Model):
    facility    = models.UUIDField(null=False, blank=False, db_comment="시설 고유번호")
    user        = models.UUIDField(null=False, blank=False, db_comment="사용자 고유번호")
    content     = models.TextField(null=False, blank=False, db_comment="내용")
    images      = models.JSONField(null=True, blank=True, db_comment="이미지 URL 배열")
    stars       = models.IntegerField(
        choices=Stars.choices,
        db_comment="별점",
        null=False,
        blank=False
    )

    class Meta:
        db_table = "facility_review"
        indexes = [
            models.Index(fields=["facility"], name="facility_review_facility_index"),
            models.Index(fields=["user"], name="facility_review_user_index"),
        ]
        verbose_name = "시설 리뷰"
        verbose_name_plural = "시설 리뷰"

class FacilityLike(models.Model):
    facility    = models.UUIDField(null=False, blank=False, db_comment="시설 고유번호")
    user        = models.UUIDField(null=False, blank=False, db_comment="사용자 고유번호")

    class Meta:
        db_table = "facility_like"
        indexes = [
            models.Index(fields=["facility"], name="facility_like_facility_index"),
            models.Index(fields=["user"], name="facility_like_user_index"),
        ]
        verbose_name = "시설 좋아요"
        verbose_name_plural = "시설 좋아요"
