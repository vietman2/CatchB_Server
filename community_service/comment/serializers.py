from django.utils import timezone, timesince
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

    def get_created_at(self, obj):
        ## 1분 미만: 방금 전
        ## 1시간 미만: n분 전
        ## 24시간 미만: n시간 전
        ## 7일 미만: n일 전
        ## 1달 미만: n주 전
        ## 1년 미만: n달 전
        ## 그 이상: n년 전
        delta = timezone.now() - obj.created_at
        if delta.seconds < 60:
            return '방금 전'
        elif delta.seconds < 3600:
            return f'{delta.seconds // 60}분 전'
        elif delta.days < 1:
            return f'{delta.seconds // 3600}시간 전'
        elif delta.days < 7:
            return f'{delta.days}일 전'
        elif delta.days < 30:
            return f'{delta.days // 7}주 전'
        elif delta.days < 365:
            return f'{delta.days // 30}달 전'
        else:
            return f'{delta.days // 365}년 전'

    def get_num_likes(self, obj):
        return obj.comment_likes.count()

    def get_num_recomments(self, obj):
        return obj.recomments.count()
