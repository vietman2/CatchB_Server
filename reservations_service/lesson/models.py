from django.db import models

class Lesson(models.Model):
    main_coach      = models.UUIDField(null=False, blank=False, db_comment="코치 고유번호")
    sub_coaches     = models.JSONField(null=True, blank=True, db_comment="보조 코치 고유번호 배열")
    reserved_user   = models.UUIDField(null=False, blank=False, db_comment="사용자 고유번호")

    ## 팀이면 팀 정보

    start_time      = models.DateTimeField(null=False, blank=False, db_comment="시작 시간")
    end_time        = models.DateTimeField(null=False, blank=False, db_comment="종료 시간")
    is_confirmed    = models.BooleanField(default=False, db_comment="예약 승인 여부")

    class Meta:
        db_table = "lesson"

class LessonReview(models.Model):
    class stars_choices(models.IntegerChoices):
        ONE     = 1, "1"
        TWO     = 2, "2"
        THREE   = 3, "3"
        FOUR    = 4, "4"
        FIVE    = 5, "5"

    ## 리뷰는 사용자가 시설에 대해 남긴다
    lesson      = models.UUIDField(null=False, blank=False, db_comment="레슨 고유번호")
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
        db_table = "lesson_review"
        indexes = [
            #TODO: 코치에 대한 인덱스 추가
            models.Index(fields=["user"], name="lesson_review_user_index"),
        ]
