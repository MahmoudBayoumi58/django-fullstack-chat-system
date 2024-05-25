from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from chat_app.models import ChatRoom, Message


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

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )

    # Receive a message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = Message.objects.create(
            chat=self.chat,
            sender=self.user,
            text=data['message']
        )
        message.save()

        data['id'] = message.id
        data['sender'] = self.user.get_full_name()
        data['sender_short_name'] = self.user.get_short_name()
        data['created_at'] = f'{message.created_at}'

        # Send a message to a room group
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {'type': 'send.message', 'data': data}
        )

    def send_message(self, event):
        self.send(json.dumps(event['data']))
