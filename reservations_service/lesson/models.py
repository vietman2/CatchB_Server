from django.db import models

class Lesson(models.Model):
    coach           = models.UUIDField(null=False, blank=False, db_comment="코치 고유번호")
    reserved_user   = models.UUIDField(null=False, blank=False, db_comment="사용자 고유번호")

    ## 팀이면 팀 정보

    start_time      = models.DateTimeField(null=False, blank=False, db_comment="시작 시간")
    end_time        = models.DateTimeField(null=False, blank=False, db_comment="종료 시간")
    is_confirmed    = models.BooleanField(default=False, db_comment="예약 승인 여부")

    class Meta:
        db_table = "lesson"
