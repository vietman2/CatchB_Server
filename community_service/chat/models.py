from django.db import models

class ChatRoomManager(models.Manager):
    def check_chatroom(self, user_uuid, other_uuid):
        # check if chatroom with user_uuid and other_uuid exists
        return self.get_queryset().filter(
            members__user_uuid=user_uuid,
        ).filter(
            members__user_uuid=other_uuid
        ).distinct().first()

    def get_chatrooms(self, user_uuid):
        # get chatrooms with user_uuid
        # should exclude chatrooms with left_members
        return self.get_queryset().filter(
            members__user_uuid=user_uuid
        ).exclude(
            left_members__user_uuid=user_uuid
        ).order_by('-updated_at')

    def get_chatroom_name(self, id, user_uuid):
        # get chatroom name
        chatroom = self.get_queryset().get(id=id)
        if chatroom.name:
            return chatroom.name

        # return the other user's name
        return chatroom.members.exclude(user_uuid=user_uuid).first().user_name

    def delete_chatroom(self, id, user_uuid):
        # get chatroom with id
        chatroom = self.get_queryset().get(id=id)
        # add user_uuid to left_members
        chatroom.left_members.add(user_uuid)

class ChatMember(models.Model):
    user_uuid   = models.UUIDField(primary_key=True, editable=False, db_comment="채팅방 멤버")
    user_name   = models.CharField(max_length=100, db_comment="채팅방 멤버 이름")
    is_active   = models.BooleanField(default=False, db_comment="서비스 탈퇴 여부")

    objects = models.Manager()

    class Meta:
        db_table            = "chat_member"
        db_table_comment    = "채팅방 멤버"

class ChatRoom(models.Model):
    name        = models.CharField(max_length=100, null=True, db_comment="채팅방 이름")
    created_at  = models.DateTimeField(auto_now_add=True, db_comment="채팅방 생성일")
    updated_at  = models.DateTimeField(auto_now=True, db_comment="채팅방 수정일")

    members     = models.ManyToManyField(ChatMember, related_name="chatroom")
    room_image = models.ImageField(
        upload_to="chatroom/",
        db_comment="채팅방 이미지",
        default="chatroom/default.png"
    )

    left_members = models.ManyToManyField(ChatMember, related_name="left_chatroom", blank=True)

    objects = ChatRoomManager()

    class Meta:
        db_table            = "chatroom"
        db_table_comment    = "채팅방"

class ChatMessage(models.Model):
    dialog      = models.ForeignKey(
        ChatRoom,
        editable=False,
        on_delete=models.SET_NULL,
        db_comment="채팅방",
        null=True
    )
    writer      = models.UUIDField(editable=False, db_comment="채팅 메시지 작성자")
    message     = models.TextField(editable=False, db_comment="채팅 메시지")
    created_at  = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        db_comment="채팅 메시지 작성일"
    )

    deleted     = models.BooleanField(default=False, db_comment="채팅 메시지 삭제 여부")
    read        = models.BooleanField(default=False, db_comment="채팅 메시지 읽음 여부")

    class Meta:
        db_table            = "chat_message"
        db_table_comment    = "채팅 메시지"
