from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

from post.models import Post
from .models import Comment
from .serializers import (
    CommentCreateSerializer, CommentListSerializer,
    CommentLikeSerializer
)

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    http_method_names = ['post', 'get']

    @extend_schema(summary='댓글 작성', tags=['댓글'])
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        except ValidationError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(summary='댓글 목록 조회', tags=['댓글'])
    def list(self, request, *args, **kwargs):
        if 'post_id' not in request.query_params:
            return Response('post_id를 입력해주세요.', status=status.HTTP_400_BAD_REQUEST)

        post_id = request.query_params['post_id']
        post = Post.objects.filter(id=post_id).first()

        if not post:
            return Response('존재하지 않는 게시글입니다.', status=status.HTTP_400_BAD_REQUEST)

        ## TODO: pagination
        comments = self.queryset.filter(post=post)
        serializer = CommentListSerializer(comments, many=True)
        ## check if user_uuid exists in query_params
        if 'user_uuid' in request.query_params:
            serializer.context['uuid'] = request.query_params['user_uuid']

        ## return number of comments
        num_comments = comments.count()
        return Response(
            {'comments': serializer.data, 'num_comments': num_comments},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    @extend_schema(summary='댓글 좋아요', tags=['댓글'])
    def like(self, request, pk=None):   ## pylint: disable=W0613
        comment = self.get_object()

        try:
            serializer = CommentLikeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            updated_comment = serializer.like(instance=comment)

        except ValidationError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        simple_serializer = CommentListSerializer(updated_comment)
        simple_serializer.context['uuid'] = request.data['user_uuid']

        return Response(simple_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    @extend_schema(summary='댓글 싫어요', tags=['댓글'])
    def dislike(self, request, pk=None):    ## pylint: disable=W0613
        comment = self.get_object()

        try:
            serializer = CommentLikeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            updated_comment = serializer.dislike(instance=comment)

        except ValidationError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        simple_serializer = CommentListSerializer(updated_comment)
        simple_serializer.context['uuid'] = request.data['user_uuid']

        return Response(simple_serializer.data, status=status.HTTP_200_OK)
