from django.db import models

from ..core.models import TimeStampedModel
from .enums import ForumChoices

class Post(TimeStampedModel):
    forum           = models.IntegerField(choices=ForumChoices.choices)
    author_uuid     = models.UUIDField(editable=False)

    title           = models.CharField(max_length=40)
    content         = models.TextField()

    ## TODO: Add Tags

    ## TODO: Add Images

    num_clicks      = models.IntegerField(default=0)

    objects = models.Manager()

    class Meta:
        db_table = 'post'
        ordering = ['-created_at']

class Comment(TimeStampedModel):
    post            = models.ForeignKey(
        Post,
        on_delete=models.DO_NOTHING,
        related_name='comments'
    )
    commenter_uuid  = models.UUIDField(editable=False)

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

class Like(models.Model):
    user_uuid       = models.UUIDField(editable=False)

    liked_at        = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class PostLike(Like):
    post            = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = 'post_like'
        unique_together = ('post', 'user_uuid')

class CommentLike(Like):
    comment         = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        db_table = 'comment_like'
        unique_together = ('comment', 'user_uuid')

class ReCommentLike(Like):
    recomment       = models.ForeignKey(ReComment, on_delete=models.CASCADE)

    class Meta:
        db_table = 'recomment_like'
        unique_together = ('recomment', 'user_uuid')
