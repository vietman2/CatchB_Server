from django.db import models

from core.models import TimeStampedModel, Report, Like, Dislike  # pylint: disable=E0611
from post.models import Post

class Comment(TimeStampedModel):
    post            = models.ForeignKey(
        Post,
        on_delete=models.DO_NOTHING,
        related_name='comments'
    )
    commenter_uuid  = models.UUIDField()

    content         = models.TextField()

    objects = models.Manager()

    class Meta:
        db_table = 'comment'
        ordering = ['created_at']

class ReComment(TimeStampedModel):
    comment         = models.ForeignKey(
        Comment,
        on_delete=models.DO_NOTHING,
        related_name='recomments'
    )
    commenter_uuid  = models.UUIDField(editable=False)

    content         = models.TextField()

    objects = models.Manager()

    class Meta:
        db_table = 'recomment'
        ordering = ['created_at']

class CommentReport(Report):
    comment         = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'comment_report'

class ReCommentReport(Report):
    recomment       = models.ForeignKey(ReComment, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'recomment_report'

class CommentLike(Like):
    comment         = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='comment_likes'
    )

    class Meta:
        db_table = 'comment_like'
        unique_together = ('comment', 'user_uuid')

class CommentDislike(Dislike):
    comment         = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='comment_dislikes'
    )

    class Meta:
        db_table = 'comment_dislike'
        unique_together = ('comment', 'user_uuid')

class ReCommentLike(Like):
    recomment       = models.ForeignKey(ReComment, on_delete=models.CASCADE)

    class Meta:
        db_table = 'recomment_like'
        unique_together = ('recomment', 'user_uuid')

class ReCommentDislike(Dislike):
    recomment       = models.ForeignKey(ReComment, on_delete=models.CASCADE)

    class Meta:
        db_table = 'recomment_dislike'
        unique_together = ('recomment', 'user_uuid')
