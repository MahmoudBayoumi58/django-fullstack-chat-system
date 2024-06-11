from django.db import models

from chat_app.models import ChatRoom
from users_app.models import Users


# Create your models here.
class VideoCall(models.Model):
    chat = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    caller = models.ForeignKey(Users, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.chat.participants.all()[0]},{self.chat.participants.all()[1]}"
