from django import template
from chat_app.models import Message

register = template.Library()


@register.filter
def unseen_messages(chat_id, user_id):
    messages = Message.objects.filter(chat_id=chat_id, is_msg_seen=False).exclude(sender_id=user_id)
    return messages.count()
