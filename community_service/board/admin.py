from django.contrib import admin

from .models import Forum, Post, Comment, ReComment, PostLike, CommentLike, ReCommentLike

admin.site.register(Forum)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(ReComment)
admin.site.register(PostLike)
admin.site.register(CommentLike)
admin.site.register(ReCommentLike)
