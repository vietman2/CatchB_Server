from django.db import models
from django.core.exceptions import ValidationError

from core.models import TimeStampedModel, Report, Like  # pylint: disable=E0611
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
    forum           = models.IntegerField(choices=ForumChoices.choices)
    author_uuid     = models.UUIDField()

    title           = models.CharField(max_length=40)
    content         = models.TextField()

    ## TODO: Add Tags
    tags            = models.ManyToManyField(Tag)

    ## TODO: Add Images
    images          = models.ManyToManyField(Image, blank=True)

    num_clicks      = models.IntegerField(default=0)

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
    post            = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = 'post_like'
        unique_together = ('post', 'user_uuid')
