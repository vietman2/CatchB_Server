from django.db import models

class ReportReason(models.TextChoices):
    AD              = 'AD', '광고'
    SPAM            = 'SP', '스팸'
    ADULT           = 'AV', '성인물'
    VIOLENCE        = 'VI', '폭력적인 내용'
    ILLEGAL         = 'IL', '불법적인 내용'
    OTHER           = 'OT', '기타'

class ReviewStatus(models.IntegerChoices):
    SUBMITTED       = 0, '제출됨'
    UNDER_REVIEW    = 1, '검토중'
    REVIEWED        = 2, '검토 완료'

class ReportStatus(models.IntegerChoices):
    PENDING         = 0, '대기중'
    ACCEPTED        = 1, '수락됨'
    REJECTED        = 2, '거부됨'
    PARTIAL         = 3, '일부 수락됨'
