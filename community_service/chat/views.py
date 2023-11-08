import uuid
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema

from .models import ChatRoom, ChatMember
from .serializers import ChatRoomSerializer, ChatRoomCreateSerializer

class ChatRoomViewSet(ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    @extend_schema(summary="채팅방 목록 조회", tags=["채팅방"])
    def list(self, request, *args, **kwargs):
        user_uuid = request.query_params.get('user_uuid')
        queryset = ChatRoom.objects.get_chatrooms(user_uuid)
        serializer = ChatRoomSerializer(queryset, many=True, context={'request': request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @extend_schema(summary="채팅방 조회", tags=["채팅방"])
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user_uuid = request.query_params.get('user_uuid')
        serializer = ChatRoomSerializer(instance, context={'request': request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @extend_schema(summary="채팅방 생성", tags=["채팅방"])
    def create(self, request, *args, **kwargs):
        # if member is not in db, create chatmember
        user_uuid = request.data['members'][0]['user_uuid']
        user_name = request.data['members'][0]['user_name']
        other_uuid = request.data['members'][1]['user_uuid']
        other_name = request.data['members'][1]['user_name']

        if user_uuid == other_uuid:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data="Cannot create chatroom with yourself"
            )

        # validate uuid: check if uuid is valid
        try:
            uuid.UUID(user_uuid)
            uuid.UUID(other_uuid)
        except ValueError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data="Invalid uuid"
            )

        if not ChatMember.objects.filter(user_uuid=user_uuid).exists():
            ChatMember.objects.create(user_uuid=user_uuid, user_name=user_name)

        if not ChatMember.objects.filter(user_uuid=other_uuid).exists():
            ChatMember.objects.create(user_uuid=other_uuid, user_name=other_name)

        data = {
            'members': [user_uuid, other_uuid]
        }

        serializer = ChatRoomCreateSerializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=e.detail)

        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    @extend_schema(summary="채팅방 수정", tags=["채팅방"])
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ChatRoomSerializer(instance, data=request.data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=e.detail)

        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @extend_schema(summary="채팅방 삭제", tags=["채팅방"])
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user_uuid = request.query_params.get('user_uuid')
        ChatRoom.objects.delete_chatroom(instance.id, user_uuid)
        return Response(status=status.HTTP_204_NO_CONTENT)
