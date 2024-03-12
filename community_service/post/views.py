from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema

from .enums import ForumChoices
from .models import Tag, Image
from .serializers import TagSerializer, ImageSerializer

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ['get']

    @extend_schema(summary='태그 목록 조회', tags=['태그'])
    def list(self, request, *args, **kwargs):
        ## create list for each forum. get forums in their display name
        forum_tags = {}
        for forum in ForumChoices:
            forum_tags[forum.label] = self.get_serializer(self.queryset.filter(forum=forum.value), many=True).data

        return Response(forum_tags, status=status.HTTP_200_OK)

    @extend_schema(exclude=True)
    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class ImageViewSet(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    http_method_names = ['post']

    @extend_schema(summary='이미지 업로드', tags=['이미지'])
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        media_url = settings.MEDIA_URL
        image_url = serializer.instance.image.name
        abs_url = media_url + image_url

        return Response({"url": abs_url, "id": serializer.instance.pk}, status=status.HTTP_201_CREATED)
