from django.db import models

class ChatRoom(models.Model):
    name = models.CharField(max_length=100, db_comment="ChatRoom Name. 채팅방 이름")
    description = models.CharField(max_length=255, db_comment="ChatRoom Description. 채팅방 설명")
    created_at = models.DateTimeField(auto_now_add=True, db_comment="ChatRoom Created At. 채팅방 생성일")
    updated_at = models.DateTimeField(auto_now=True, db_comment="ChatRoom Updated At. 채팅방 수정일")

    ## 추후 추가할 필드
    ## 참여자
    ## 채팅방 이미지
    ## 채팅방 타입
    ## 채팅방 설정

    class Meta:
        db_table = "chatroom"
        db_table_comment = "ChatRoom. 채팅방"

class ChatMessage(models.Model):
    dialog = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, db_comment="ChatRoom. 채팅방")
    author = models.IntegerField(db_comment="ChatMessage Author. 채팅 메시지 작성자")
    message = models.TextField(db_comment="ChatMessage. 채팅 메시지")
    created_at = models.DateTimeField(auto_now_add=True, db_comment="ChatMessage Created At. 채팅 메시지 작성일")

    ## 추후 추가할 필드
    ## 채팅 메시지 읽음 여부

    class Meta:
        db_table = "chat_message"
        db_table_comment = "ChatMessage. 채팅 메시지"
