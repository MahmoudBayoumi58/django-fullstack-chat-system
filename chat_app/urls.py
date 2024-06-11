from django.urls import path
from .views import *

urlpatterns = [
    path('home', chat_home, name='chat_home'),
    path('create-chat/<str:friend_uuid>', create_chat, name='create_chat'),
    path('chatted-users', get_chatted_users, name='chatted_users'),
    path('details/<str:chat_uuid>', chat_view, name='chat_view'),
    path('video/<str:chat_uuid>', video_view, name='video_view'),
]
