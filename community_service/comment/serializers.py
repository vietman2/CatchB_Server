from django.utils import timezone
from rest_framework import serializers

from .models import Comment

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'commenter_uuid', 'content']

class CommentListSerializer(serializers.ModelSerializer):
    created_at      = serializers.SerializerMethodField()
    num_likes       = serializers.SerializerMethodField()
    num_recomments  = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'commenter_uuid',   ## TODO: change to nickname
            'content',
            'created_at',
            'num_likes',
            'num_recomments'
        ]

    def get_created_at(self, obj):  ## pylint: disable=R0911
        delta = timezone.now() - obj.created_at

        if delta.days < 1:
            if delta.seconds < 60:
                return '방금 전'
            if delta.seconds < 3600:
                return f'{delta.seconds // 60}분 전'
            return f'{delta.seconds // 3600}시간 전'
        if delta.days < 7:
            return f'{delta.days}일 전'
        if delta.days < 30:
            return f'{delta.days // 7}주 전'
        if delta.days < 365:
            return f'{delta.days // 30}달 전'

        return f'{delta.days // 365}년 전'

    def get_num_likes(self, obj):
        return obj.comment_likes.count()

    def get_num_recomments(self, obj):
        return obj.recomments.count()
