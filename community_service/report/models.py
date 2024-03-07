from django.db import models

from board.models import Post, Comment, ReComment
from core.models import TimeStampedModel
from .enums import ReportReason

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

class PostReport(Report):
    post            = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'post_report'

class CommentReport(Report):
    comment         = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'comment_report'

class ReCommentReport(Report):
    recomment       = models.ForeignKey(ReComment, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'recomment_report'
