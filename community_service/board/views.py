from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from drf_spectacular.utils import extend_schema

from .models import Forum, Post
from .serializers import ForumSerializer, ForumListSerializer, PostSerializer

class ForumViewSet(ModelViewSet):
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    http_method_names = ['get', 'post', 'delete']

    @extend_schema(summary="게시판 목록 조회", tags=["게시판"])
    def list(self, request, *args, **kwargs):
        queryset = Forum.objects.get_list()
        serializer = ForumListSerializer(queryset, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(summary="게시판 생성", tags=["게시판"])
    def create(self, request, *args, **kwargs):
        serializer = ForumSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(data={"message": e.detail}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(summary="게시판 삭제", tags=["게시판"])
    def destroy(self, request, *args, **kwargs):
        forum = self.get_object()
        Forum.objects.delete_forum(forum)
        message = {"message": "삭제되었습니다"}

        return Response(data=message, status=status.HTTP_204_NO_CONTENT)

    @extend_schema(exclude=True)
    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    http_method_names = ['get', 'post', 'delete', 'patch']

    @extend_schema(summary="게시글 목록 조회", tags=["게시글"])
    def list(self, request, *args, **kwargs):
        forum_id = request.query_params.get("forum_id")

        if not forum_id:
            return Response(data={"message": "forum_id를 입력해주세요"}, status=status.HTTP_400_BAD_REQUEST)

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
