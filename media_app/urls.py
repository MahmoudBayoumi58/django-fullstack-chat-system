from django.urls import path
from .views import *

urlpatterns = [
    path('send/image/<str:chat_uuid>/', send_image, name='send_image'),
    path('send/audio/<str:chat_uuid>/', send_audio, name='send_audio'),
]
