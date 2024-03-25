from django.core.files.storage import default_storage
from django.utils import timezone
from rest_framework import serializers

from comment.serializers import CommentListSerializer
from .models import Tag, Image, Post, PostContentView

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'icon', 'color', 'bgcolor']

class ImageSerializer(serializers.ModelSerializer):
    user_uuid = serializers.UUIDField(write_only=True)
    image = serializers.FileField()

    class Meta:
        model = Image
        fields = ['image', 'user_uuid']

    def save(self, **kwargs):
        uuid = self.validated_data['user_uuid']
        image = self.validated_data['image']

        ## TODO: 파일 경로/이름을 무작위로 생성하도록 수정
        path = f'community/{uuid}/{image.name}'
        filename = default_storage.save(path, image)
        self.instance = Image.objects.create(image=filename)

        return self.instance

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['forum', 'author_uuid', 'title', 'content', 'tags', 'images']

    def validate_tags(self, value):
        if len(value) > 3:
            raise serializers.ValidationError('게시글은 최대 3개의 태그를 가질 수 있습니다.')
        return value

class PostSimpleSerializer(serializers.ModelSerializer):
    contains_images = serializers.SerializerMethodField()
    num_likes       = serializers.SerializerMethodField()
    num_dislikes    = serializers.SerializerMethodField()
    num_comments    = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'author_uuid',  ## TODO: Replace uuid with nickname by requesting user service
            'title',
            'content',
            'tags',
            'contains_images',
            'num_clicks',
            'created_at',
            'num_likes',
            'num_dislikes',
            'num_comments'
        ]

    def get_contains_images(self, obj):
        if obj.images.exists():
            return True

        return False

    def get_num_likes(self, obj):
        return obj.post_likes.count()
    
    def get_num_dislikes(self, obj):
        return obj.post_dislikes.count()

    def get_num_comments(self, obj):
        return obj.comments.count()

class PostDetailSerializer(serializers.ModelSerializer):
    tags            = TagSerializer(many=True)
    images          = ImageSerializer(many=True)
    forum           = serializers.CharField(source='get_forum_display')
    num_likes       = serializers.SerializerMethodField()
    num_comments    = serializers.SerializerMethodField()
    comments        = CommentListSerializer(many=True)  # TODO: Add pagination

    class Meta:
        model = Post
        fields = [
            'id',
            'forum',
            'author_uuid',  ## TODO: Replace uuid with nickname by requesting user service
            'title',
            'content',
            'tags',
            'images',
            'num_clicks',
            'created_at',
            'updated_at',
            'num_likes',
            'num_comments',
            'comments'
        ]

    def increment_clicks(self):
        self.instance.num_clicks += 1
        self.instance.save()

    def content_viewed(self, user_uuid):
        view_obj = PostContentView.objects.filter(post=self.instance, user_uuid=user_uuid).first()

        if view_obj is None:
            PostContentView.objects.create(post=self.instance, user_uuid=user_uuid)
        else:
            view_obj.viewed_last_at = timezone.now()
            view_obj.save()

        return True

    def get_num_likes(self, obj):
        return obj.post_likes.count()

    def get_num_comments(self, obj):
        return obj.comments.count()
