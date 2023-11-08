from django.urls import path

from chat.consumers import ChatConsumer

websocket_urlpatterns = [
    path("ws/chat/<int:room_id>", ChatConsumer.as_asgi()),
]