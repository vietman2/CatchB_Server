from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

from .models import Post, Comment, ReComment
from .serializers import (
    PostSerializer,
    CommentSerializer, ReCommentSerializer,
    PostLikeSerializer, CommentLikeSerializer, ReCommentLikeSerializer
)

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    http_method_names = ['get', 'post', 'delete', 'patch']

    @extend_schema(summary="게시글 목록 조회", tags=["게시글"])
    def list(self, request, *args, **kwargs):
        forum_id = request.query_params.get("forum_id")

        if not forum_id:
            return Response(data={"message": "게시판을 입력해주세요"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Post.objects.get_list(forum_id)
        serializer = PostSerializer(queryset, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(summary="게시글 삭제", tags=["게시글"])
    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        Post.objects.delete_post(post)
        message = {"message": "삭제되었습니다"}

        return Response(data=message, status=status.HTTP_204_NO_CONTENT)

    @extend_schema(summary="게시글 작성", tags=["게시글"])
    def create(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.validate_create(serializer.validated_data)
        except ValidationError as e:
            return Response(data={"message": e.detail}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(summary="게시글 수정", tags=["게시글"])
    def partial_update(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = PostSerializer(post, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.validate_partial_update(serializer.validated_data)
        except ValidationError as e:
            return Response(data={"message": e.detail}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(summary="게시글 좋아요", tags=["게시글"])
    @action(detail=True, methods=["post"])
    # pylint: disable=W0613
    def like(self, request, *args, **kwargs):
        serializer = PostLikeSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(data={"message": e.detail}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data={"message": "좋아요되었습니다"}, status=status.HTTP_200_OK)

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    http_method_names = ['post']

    @extend_schema(summary="댓글 좋아요", tags=["댓글"])
    @action(detail=True, methods=["post"])
    # pylint: disable=W0613
    def like(self, request, *args, **kwargs):
        serializer = CommentLikeSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(data={"message": e.detail}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data={"message": "좋아요되었습니다"}, status=status.HTTP_200_OK)

class ReCommentViewSet(ModelViewSet):
    queryset = ReComment.objects.all()
    serializer_class = ReCommentSerializer
    http_method_names = ['post']

    @extend_schema(summary="대댓글 좋아요", tags=["대댓글"])
    @action(detail=True, methods=["post"])
    # pylint: disable=W0613
    def like(self, request, *args, **kwargs):
        serializer = ReCommentLikeSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(data={"message": e.detail}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data={"message": "좋아요되었습니다"}, status=status.HTTP_200_OK)
