from rest_framework import serializers

from .models import (
    Forum, Post, Comment, ReComment, PostLike, CommentLike,
    ReCommentLike, Bookmark, PostReport, CommentReport, ReCommentReport
)

class ForumListSerializer(serializers.ModelSerializer):
    latest_post = serializers.SerializerMethodField()

    def get_latest_post(self, obj):
        latest_post = Post.objects.filter(forum_id=obj.id).last()
        if latest_post:
            return latest_post.title
        else:
            return None

    class Meta:
        model = Forum
        fields = ["forum_name", "latest_post"]

class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = '__all__'

class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "author_uuid", "created_at", "num_shares", "num_clicks"]

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
