from django.urls import path
from chat_app.websocket.consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<str:chat_uuid>/', ChatConsumer.as_asgi())
]
