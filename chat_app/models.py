from django.db import models
import uuid
from users_app.models import Users
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
class ChatRoom(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    participants = models.ManyToManyField(Users, related_name='chat_rooms')
    last_msg = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.participants.all()[0]},{self.participants.all()[1]}"


class Message(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(Users, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    audio = models.FileField(upload_to='chat-audio', null=True, blank=True)
    image = models.ImageField(upload_to='chat-images', null=True, blank=True)
    is_msg_seen = models.BooleanField(default=False)

    def __str__(self):
        return str(self.chat)


@receiver(post_save, sender=Message)
def update_last_message(created, instance, **kwargs):
    if created:
        if instance.text:
            msg = f'{instance.text}'

        else:
            msg = f'Media'

        instance.chat.last_msg = msg
        instance.chat.save()

