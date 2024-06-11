from channels.layers import get_channel_layer
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from asgiref.sync import async_to_sync

from chat_app.models import ChatRoom, Message


# Create your views here.
@login_required
def send_image(request, chat_uuid):
    data = {}
    chat = get_object_or_404(ChatRoom, uuid=chat_uuid)
    sender = request.user
    image = request.FILES['image']
    group_name = f'chat_{chat_uuid}'

    message = Message(
        chat=chat,
        sender=sender,
        image=image
    )
    message.save()

    data['id'] = message.id
    data['sender'] = sender.get_full_name()
    data['sender_short_name'] = sender.get_short_name()
    data['action'] = 'createMessage'
    data['created_at'] = f'{message.created_at}'
    data['image'] = message.image.url

    event = {
        'type': 'send.message',
        'data': data
    }

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name, event
    )

    return HttpResponse('Done')


@login_required
def send_audio(request, chat_uuid):
    data = {}
    chat = get_object_or_404(ChatRoom, uuid=chat_uuid)
    sender = request.user
    audio = request.FILES['audio']
    audio.name = 'blob.ogg'
    group_name = f'chat_{chat_uuid}'

    message = Message(
        chat=chat,
        sender=sender,
        audio=audio
    )
    message.save()

    data['id'] = message.id
    data['sender'] = sender.get_full_name()
    data['sender_short_name'] = sender.get_short_name()
    data['action'] = 'createMessage'
    data['created_at'] = f'{message.created_at}'
    data['audio'] = message.audio.url

    event = {
        'type': 'send.message',
        'data': data
    }

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name, event
    )

    return HttpResponse('Done')
