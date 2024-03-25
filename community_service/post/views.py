from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

from .enums import ForumChoices
from .models import Tag, Image, Post
from .serializers import (
    TagSerializer, ImageSerializer,
    PostCreateSerializer, PostSimpleSerializer,
    PostDetailSerializer, PostLikeSerializer
)

def getForum(text):
    if text == '덕아웃':
        return ForumChoices.DUGOUT
    if text == '드래프트':
        return ForumChoices.RECRUIT
    if text == '장터':
        return ForumChoices.MARKET
    if text == "스틸":
        return ForumChoices.STEAL

    raise ValidationError("존재하지 않는 게시판입니다.")

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ['get']

    @extend_schema(exclude=True)
    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(summary='태그 목록 조회', tags=['태그'])
    def list(self, request, *args, **kwargs):
        ## create list for each forum. get forums in their display name
        forum_tags = {}
        for forum in ForumChoices:
            forum_tags[forum.label] = self.get_serializer(
                self.queryset.filter(forum=forum.value),
                many=True
            ).data

        return Response(forum_tags, status=status.HTTP_200_OK)

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

        return Response(
            {"url": abs_url, "id": serializer.instance.pk},
            status=status.HTTP_201_CREATED
        )

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    http_method_names = ['get', 'post']

    @extend_schema(summary='게시글 작성', tags=['게시글'])
    def create(self, request, *args, **kwargs):
        data = request.data
        data['forum'] = getForum(data['forum'])

        try:
            serializer = PostCreateSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        except ValidationError as e:
            if 'unique' in str(e):
                return Response({'message': "이미 존재하는 게시글입니다."}, status=status.HTTP_400_BAD_REQUEST)

            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(summary='게시글 목록 조회', tags=['게시글'])
    def list(self, request, *args, **kwargs):
        if 'forum' in request.query_params:
            forum = getForum(request.query_params['forum'])
            queryset = self.queryset.filter(forum=forum, is_deleted=False, is_under_review=False)

            serializer = PostSimpleSerializer(queryset, many=True)

            tags = Tag.objects.filter(forum=forum)
            tags = TagSerializer(tags, many=True).data

            ## TODO: Pagination 구현
            return Response({"posts": serializer.data, "tags": tags}, status=status.HTTP_200_OK)

        ## TODO: 내가 쓴 글만 보기 구현
        return Response({'message': "게시판을 선택해주세요."}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(summary='게시글 상세 조회', tags=['게시글'])
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PostDetailSerializer(instance)
        serializer.context['uuid'] = request.query_params.get('uuid', None)
        serializer.increment_clicks()

        uuid = request.query_params.get('uuid', None)
        if uuid is not None:
            serializer.content_viewed(uuid)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    @extend_schema(summary='게시글 좋아요', tags=['게시글'])
    def like(self, request, pk=None):
        instance = self.get_object()

        try:
            serializer = PostLikeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            updated_instance = serializer.like(instance=instance)

        except ValidationError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        detail_serializer = PostDetailSerializer(updated_instance)
        detail_serializer.context['uuid'] = request.data['user_uuid']

        return Response(detail_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    @extend_schema(summary='게시글 싫어요', tags=['게시글'])
    def dislike(self, request, pk=None):
        instance = self.get_object()

        try:
            serializer = PostLikeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            updated_instance = serializer.dislike(instance=instance)

        except ValidationError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        detail_serializer = PostDetailSerializer(updated_instance)
        detail_serializer.context['uuid'] = request.data['user_uuid']

        return Response(detail_serializer.data, status=status.HTTP_200_OK)
