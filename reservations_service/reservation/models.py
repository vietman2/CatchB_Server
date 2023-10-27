from django.db import models

class Reservation(models.Model):
    facility        = models.UUIDField(null=False, blank=False, db_comment="시설 고유번호")
    reserved_user   = models.UUIDField(null=False, blank=False, db_comment="사용자 고유번호")

    ## 레슨이랑 연결 가능
    ## lesson = models.ForeignKey("lesson.Lesson",
    # on_delete=models.DO_NOTHING,
    # db_comment="레슨 고유번호"
    # )

    start_time      = models.DateTimeField(null=False, blank=False, db_comment="시작 시간")
    end_time        = models.DateTimeField(null=False, blank=False, db_comment="종료 시간")
    is_confirmed    = models.BooleanField(default=False, db_comment="예약 승인 여부")

    class Meta:
        db_table = "reservation"
