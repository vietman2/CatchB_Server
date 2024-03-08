from django.db import models

from .enums import ReportReason

class TimeStampedModel(models.Model):
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    is_deleted      = models.BooleanField(default=False)
    deleted_at      = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

class Like(models.Model):
    user_uuid       = models.UUIDField(editable=False)

    liked_at        = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Report(TimeStampedModel):
    report_user_uuid    = models.UUIDField(editable=False)
    report_content      = models.TextField()
    report_reason       = models.CharField(
        max_length=2,
        choices=ReportReason.choices,
        default=ReportReason.OTHER
    )

    reviewed            = models.BooleanField(default=False)
    feedback            = models.TextField(null=True)

    class Meta:
        abstract = True
