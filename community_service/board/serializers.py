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

    def validate_create(self, data):
        forum = data.get("forum")
        if not forum:
            raise serializers.ValidationError("forum을 입력해주세요")

        return data

    def validate_partial_update(self, data):
        ## forum and authod_uuid cannot be updated
        forum = data.get("forum")
        author_uuid = data.get("author_uuid")

        if forum:
            raise serializers.ValidationError("forum은 수정할 수 없습니다")

        if author_uuid:
            raise serializers.ValidationError("author_uuid는 수정할 수 없습니다")

        title = data.get("title")
        content = data.get("content")

        if not title and not content:
            raise serializers.ValidationError("수정할 내용이 없습니다")

    def validate_forum(self, forum):
        if forum.is_deleted:
            raise serializers.ValidationError("삭제된 게시판입니다")

        return forum

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ReCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReComment
        fields = '__all__'

class PostReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReport
        fields = '__all__'

class CommentReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReport
        fields = '__all__'

class ReCommentReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReCommentReport
        fields = '__all__'

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = '__all__'

class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = '__all__'

class ReCommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReCommentLike
        fields = '__all__'
