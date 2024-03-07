from django.db import models

class ReportReason(models.TextChoices):
    AD              = 'AD', '광고'
    SPAM            = 'SP', '스팸'
    ADULT           = 'AV', '성인물'
    VIOLENCE        = 'VI', '폭력적인 내용'
    ILLEGAL         = 'IL', '불법적인 내용'
    OTHER           = 'OT', '기타'
