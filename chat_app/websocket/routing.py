from django.urls import path
from chat_app.websocket.consumers import ChatConsumer, CallConsumer

websocket_urlpatterns = [
    path('ws/chat/<str:chat_uuid>/', ChatConsumer.as_asgi()),
    path('ws/call/<str:chat_uuid>/', CallConsumer.as_asgi()),
]
