from django.db import models

class ForumCategory(models.TextChoices):
    RECRUITMENT  = "RECRUIT", "모집"
    INFORMATION = "INFO", "정보"
    FREE        = "FREE", "자유"

class ForumManager(models.Manager):
    def delete_forum(self, forum):
        forum.is_deleted = True
        forum.save(using=self._db)

        return self

    def get_list(self):
        return super().get_queryset().filter(is_deleted=False)

class Forum(models.Model):
    forum_name      = models.CharField(max_length=100, unique=True)
    category        = models.CharField(
        choices=ForumCategory.choices,
        max_length=10,
        default=ForumCategory.FREE,
        editable=False
    )
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

class CommentManager(models.Manager):
    def create(self, post, author_uuid, content, anonymous=False):
        comment = super().create(
            post=post,
            author_uuid=author_uuid,
            content=content,
            anonymous=anonymous
        )

        return comment

class Comment(models.Model):
    post            = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    author_uuid     = models.UUIDField()

    content         = models.TextField()
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    anonymous       = models.BooleanField(default=False)

    objects = CommentManager()

    class Meta:
        db_table = 'comment'
        ordering = ['created_at']

class ReCommentManager(models.Manager):
    def create(self, comment, author_uuid, content, anonymous=False):
        recomment = super().create(
            comment=comment,
            author_uuid=author_uuid,
            content=content,
            anonymous=anonymous
        )

        return recomment

class ReComment(models.Model):
    comment         = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)
    author_uuid     = models.UUIDField()

    content         = models.TextField()
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    anonymous       = models.BooleanField(default=False)

    objects = ReCommentManager()

    class Meta:
        db_table = 'recomment'
        ordering = ['created_at']

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

class ReportReason(models.TextChoices):
    SPAM            = 'SP', '스팸'
    ADULT           = 'AD', '성인물'
    VIOLENCE        = 'VI', '폭력적인 내용'
    ILLEGAL         = 'IL', '불법적인 내용'
    OTHER           = 'OT', '기타'

class PostReport(models.Model):
    post            = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    report_user_uuid= models.UUIDField()
    report_content  = models.TextField()
    report_reason   = models.CharField(
        max_length=2,
        choices=ReportReason.choices,
        default=ReportReason.OTHER
    )

class CommentReport(models.Model):
    comment         = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True)
    report_user_uuid= models.UUIDField()
    report_content  = models.TextField()
    report_reason   = models.CharField(
        max_length=2,
        choices=ReportReason.choices,
        default=ReportReason.OTHER
    )

class ReCommentReport(models.Model):
    recomment       = models.ForeignKey(ReComment, on_delete=models.SET_NULL, null=True)
    report_user_uuid= models.UUIDField()
    report_content  = models.TextField()
    report_reason   = models.CharField(
        max_length=2,
        choices=ReportReason.choices,
        default=ReportReason.OTHER
    )
