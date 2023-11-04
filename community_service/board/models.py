from django.db import models

class Forum(models.Model):
    forum_name      = models.CharField(max_length=100)
    created_at      = models.DateTimeField(auto_now_add=True)
    created_by      = models.CharField(max_length=100)
    moderator       = models.CharField(max_length=100)
    allow_anonymous = models.BooleanField(default=False)

class Post(models.Model):
    forum_id        = models.ForeignKey(Forum, on_delete=models.SET_NULL, null=True)
    author_uuid     = models.UUIDField()

    title           = models.CharField(max_length=100)
    content         = models.TextField()

    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    anonymous       = models.BooleanField(default=False)
    num_shares      = models.IntegerField(default=0)
    num_shares      = models.IntegerField(default=0)

class Comment(models.Model):
    post_id         = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    author_uuid     = models.UUIDField()

    comment         = models.TextField()
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    anonymous       = models.BooleanField(default=False)

class ReComment(models.Model):
    comment_id      = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)
    author_uuid     = models.UUIDField()

    comment         = models.TextField()
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    anonymous       = models.BooleanField(default=False)

class PostLike(models.Model):
    post_id         = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    like_user_uuid  = models.UUIDField()

class CommentLike(models.Model):
    comment_id      = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)
    like_user_uuid  = models.UUIDField()

class ReCommentLike(models.Model):
    recomment_id    = models.ForeignKey(ReComment, on_delete=models.SET_NULL, null=True)
    like_user_uuid  = models.UUIDField()
