from django.db import models
from django.utils.translation import gettext_lazy as _

class Coach(models.Model):
    coach_uuid = models.UUIDField(db_comment="시설 소유자 유저번호")

    # certification = models.FileField(db_comment='자격증', help_text='자격증을 첨부해주세요.')
    academic_background = models.TextField(db_comment='학력', help_text='학력을 입력해주세요.')
    baseball_career = models.TextField(db_comment='야구 경력', help_text='야구 경력을 입력해주세요.')
    coaching_career = models.TextField(db_comment='코칭 경력', help_text='코칭 경력을 입력해주세요.')
    # facility = models.TextField(db_comment="소속 시설")
    # areas = models.TextField(db_comment="레슨 영역", help_text="레슨 영역: 타격, 투구, 수비, 주루, 트레이닝, 피지컬, 기타")

    is_approved = models.BooleanField(default=False, db_comment='코치 승인 여부')

    objects = models.Manager()

    class Meta:
        db_table = 'coach'
        verbose_name = _('coach')
        verbose_name_plural = _('coaches')
