from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json
from chat_app.models import ChatRoom, Message
from asgiref.sync import sync_to_async
from django.utils import timezone
from media_app.models import VideoCall


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope['user']

        if self.user.is_anonymous:
            self.close()
            return

        chat_uuid = self.scope['url_route']['kwargs']['chat_uuid']
        self.group_name = f'chat_{chat_uuid}'

        self.chat = ChatRoom.objects.get(uuid=chat_uuid)

        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )

        self.accept()
        self.mark_messages_as_read()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )

    # Receive a message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        data['sender'] = self.user.get_full_name()
        data['sender_short_name'] = self.user.get_short_name()

        if data['action'] == 'createMessage':
            message = Message.objects.create(
                chat=self.chat,
                sender=self.user,
                text=data['message']
            )
            message.save()

            data['id'] = message.id
            data['created_at'] = f'{message.created_at}'

        elif data['action'] == 'editMessage':
            message = self.edit_message(data['message_id'], data['message'])
            data['id'] = message.id
            data['created_at'] = f'{message.created_at}'

        elif data['action'] == 'deleteMessage':
            self.delete_message(data['message_id'])

        # Send a message to a room group
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {'type': 'send.message', 'data': data}
        )

    def send_message(self, event):
        self.send(json.dumps(event['data']))

    def edit_message(self, msg_id, new_message):
        message = Message.objects.get(id=msg_id)
        message.text = new_message
        message.created_at = timezone.now()
        message.save()
        return message

    def delete_message(self, msg_id):
        message = Message.objects.get(id=msg_id)
        message.delete()

    def mark_messages_as_read(self):
        messages = Message.objects.filter(chat=self.chat, is_msg_seen=False).exclude(sender=self.user)
        messages.update(is_msg_seen=True)


class CallConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']

        if self.user.is_anonymous:
            await self.close()
            return

        self.chat_uuid = self.scope['url_route']['kwargs']['chat_uuid']
        self.group_name = f'call_{self.chat_uuid}'

        await self.channel_layer.group_add(
            self.group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name, self.channel_name
        )

    # Receive a message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        if data['action'] == 'videoCall':
            if data['type'] == 'offer':
                data = data['offer']

            elif data['type'] == 'answer':
                data = data['answer']

            elif data['type'] == 'candidate':
                data = {"candidate": data['candidate'], "from": data['from']}

            elif data['type'] == 'close':
                await self.close_call(self.chat_uuid)

        # Send a message to a room group
        await self.channel_layer.group_send(
            self.group_name, {'type': 'call.message', 'data': data}
        )

    async def call_message(self, event):
        await self.send(json.dumps(event['data']))

    @sync_to_async
    def close_call(self, chat_uuid):
        chat = ChatRoom.objects.get(uuid=chat_uuid)
        VideoCall.objects.get(room=chat).delete()
