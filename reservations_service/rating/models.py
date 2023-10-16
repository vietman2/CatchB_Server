from django.db import models

class FacilityReview(models.Model):
    class stars_choices(models.IntegerChoices):
        ONE     = 1, "1"
        TWO     = 2, "2"
        THREE   = 3, "3"
        FOUR    = 4, "4"
        FIVE    = 5, "5"

    ## 리뷰는 사용자가 시설에 대해 남긴다
    facility    = models.UUIDField(null=False, blank=False, db_comment="시설 고유번호")
    user        = models.UUIDField(null=False, blank=False, db_comment="사용자 고유번호")
    content     = models.TextField(null=False, blank=False, db_comment="내용")
    images      = models.JSONField(null=True, blank=True, db_comment="이미지 URL 배열")
    stars       = models.IntegerField(
        choices=stars_choices.choices,
        db_comment="별점",
        null=False,
        blank=False
    )

    class Meta:
        db_table = "review"
        indexes = [
            models.Index(fields=["facility"], name="facility_index"),
            models.Index(fields=["user"], name="user_index"),
        ]
