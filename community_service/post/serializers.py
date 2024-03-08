from rest_framework import serializers

from .models import Tag

class TagSerializer(serializers.ModelSerializer):
    forum = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['forum', 'name']

    def get_forum(self, obj):
        return obj.get_forum_display()
