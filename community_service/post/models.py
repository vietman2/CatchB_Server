from django.db import models

from core.models import (  # pylint: disable=E0611
    TimeStampedModel, Report, Like,
    Dislike, CustomAutoField)
from .enums import ForumChoices

class Tag(models.Model):
    forum           = models.IntegerField(choices=ForumChoices.choices)
    name            = models.CharField(max_length=20)

    icon            = models.URLField()
    color           = models.CharField(max_length=7)
    bgcolor         = models.CharField(max_length=7)

    objects = models.Manager()

    class Meta:
        db_table = 'tag'
        ordering = ['name']

class Image(TimeStampedModel):
    image           = models.FileField(null=True)

    objects = models.Manager()

    class Meta:
        db_table = 'image'

class Post(TimeStampedModel):
    id              = CustomAutoField()
    forum           = models.IntegerField(choices=ForumChoices.choices)
    author_uuid     = models.UUIDField()

    title           = models.CharField(max_length=40)
    content         = models.TextField()

    tags            = models.ManyToManyField(Tag)
    images          = models.ManyToManyField(Image, blank=True)

    num_clicks      = models.IntegerField(default=0)
    is_under_review = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        db_table = 'post'
        ordering = ['-created_at']
        unique_together = ('forum', 'author_uuid', 'title')

class Steal(Post):
    video        = models.FileField(upload_to='steal_videos')

    class Meta:
        db_table = 'steal'

class PostReport(Report):
    post            = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'post_report'

class PostLike(Like):
    post            = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')

    class Meta:
        db_table = 'post_like'
        unique_together = ('post', 'user_uuid')

class PostDislike(Dislike):
    post            = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='post_dislikes'
    )

    class Meta:
        db_table = 'post_dislike'
        unique_together = ('post', 'user_uuid')

class PostContentView(models.Model):
    post            = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_uuid       = models.UUIDField()
    viewed_first_at = models.DateTimeField(auto_now_add=True)
    viewed_last_at  = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        db_table = 'content_view'
        unique_together = ('post', 'user_uuid')
