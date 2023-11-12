from django.db import models

class ForumManager(models.Manager):
    def delete_forum(self, forum):
        forum.is_deleted = True
        forum.save(using=self._db)

        return self

    def get_list(self):
        return super().get_queryset().filter(is_deleted=False)

class Forum(models.Model):
    forum_name      = models.CharField(max_length=100, unique=True)
    created_at      = models.DateTimeField(auto_now_add=True, editable=False)
    allow_anonymous = models.BooleanField(default=False, editable=False)
    is_deleted      = models.BooleanField(default=False)

    objects = ForumManager()

    class Meta:
        db_table = 'forum'
        ordering = ['created_at']

class PostManager(models.Manager):
    def delete_post(self, post):
        post.is_deleted = True
        post.save(using=self._db)

        return self

    def get_list(self, forum_id):
        return super().get_queryset().filter(forum_id=forum_id, is_deleted=False)

class Post(models.Model):
    forum           = models.ForeignKey(Forum, on_delete=models.SET_NULL, null=True)
    author_uuid     = models.UUIDField()

    title           = models.CharField(max_length=100)
    content         = models.TextField()

    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    anonymous       = models.BooleanField(default=False)
    num_shares      = models.IntegerField(default=0)
    num_clicks      = models.IntegerField(default=0)

    is_deleted      = models.BooleanField(default=False)

    objects = PostManager()

    class Meta:
        db_table = 'post'
        ordering = ['-created_at']

class Comment(models.Model):
    post            = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    author_uuid     = models.UUIDField()

    comment         = models.TextField()
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    anonymous       = models.BooleanField(default=False)

class ReComment(models.Model):
    comment         = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)
    author_uuid     = models.UUIDField()

    comment         = models.TextField()
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    anonymous       = models.BooleanField(default=False)

class PostLike(models.Model):
    post            = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    like_user_uuid  = models.UUIDField()

class CommentLike(models.Model):
    comment         = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)
    like_user_uuid  = models.UUIDField()

class ReCommentLike(models.Model):
    recomment       = models.ForeignKey(ReComment, on_delete=models.SET_NULL, null=True)
    like_user_uuid  = models.UUIDField()

class Bookmark(models.Model):
    user_uuid       = models.UUIDField()
    post            = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)

class PostReport(models.Model):
    post            = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    report_user_uuid= models.UUIDField()
    report_content  = models.TextField()

class CommentReport(models.Model):
    comment         = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)
    report_user_uuid= models.UUIDField()
    report_content  = models.TextField()

class ReCommentReport(models.Model):
    recomment       = models.ForeignKey(ReComment, on_delete=models.SET_NULL, null=True)
    report_user_uuid= models.UUIDField()
    report_content  = models.TextField()
