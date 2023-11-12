from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from .models import ChatRoom, ChatMessage

class ChatRoomSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    @extend_schema_field(serializers.CharField())
    def get_last_message(self, obj):
        last_message = ChatMessage.objects.filter(dialog=obj).last()
        if last_message:
            return last_message.message
        else:
            return None

    @extend_schema_field(serializers.CharField())
    def get_name(self, obj):
        request = self.context.get('request')
        user_uuid = request.query_params.get('user_uuid')
        if user_uuid:
            name = ChatRoom.objects.get_chatroom_name(obj.id, user_uuid)
            return name
        else:
            raise serializers.ValidationError("user_uuid is required")

    class Meta:
        model = ChatRoom
        fields = [
            'id',
            'name',
            'created_at',
            'updated_at',
            'members',
            'room_image',
            'last_message',
        ]

class ChatRoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'

    def validate_members(self, value):
        # check if chatroom with same members exists
        user_uuid = value[0].user_uuid
        other_uuid = value[1].user_uuid

        if ChatRoom.objects.check_chatroom(user_uuid, other_uuid):
            raise serializers.ValidationError("Chatroom already exists")

        return value
