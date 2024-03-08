from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema

from .models import Tag
from .serializers import TagSerializer

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ['get']

    @extend_schema(summary='태그 목록 조회', tags=['태그'])
    def list(self, request, *args, **kwargs):
        ## create list for each forum. get forums in their display name
        forum_tags = {}
        for tag in self.queryset:
            forum = tag.get_forum_display()
            if forum not in forum_tags:
                forum_tags[forum] = []
            forum_tags[forum].append(tag.name)

        return Response(forum_tags, status=status.HTTP_200_OK)

    @extend_schema(exclude=True)
    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
