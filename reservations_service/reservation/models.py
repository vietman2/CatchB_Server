import uuid
from django.db import models

class StatusChoices(models.TextChoices):
    WAITING     = "WAITING", "대기"
    CONFIRMED   = "CONFIRMED", "승인"
    CANCELLED   = "CANCELLED", "취소"
    FINISHED    = "FINISHED", "완료"

class Reservation(models.Model):
    uuid            = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_comment="예약 고유번호"
    )
    facility        = models.UUIDField(null=False, blank=False, db_comment="시설 고유번호")
    reserved_user   = models.UUIDField(null=False, blank=False, db_comment="사용자 고유번호")

    ## 레슨이랑 연결 가능
    ## lesson = models.ForeignKey("lesson.Lesson",
    # on_delete=models.DO_NOTHING,
    # db_comment="레슨 고유번호"
    # )

    date            = models.DateField(null=False, blank=False, db_comment="예약 날짜")
    start_time      = models.TimeField(null=False, blank=False, db_comment="시작 시간")
    end_time        = models.TimeField(null=False, blank=False, db_comment="종료 시간")
    status          = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.WAITING,
        db_comment="예약 상태"
    )

    class Meta:
        db_table = "reservation"
        ordering = ['date', 'start_time']
        verbose_name = "예약"
        verbose_name_plural = "예약"
