from django.core.files.storage import default_storage
from rest_framework import serializers

from .models import Tag, Image, Post

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
