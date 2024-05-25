from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from chat_app.models import ChatRoom, Message
from users_app.models import Users


# Create your views here.
@login_required
def create_chat(request, friend_uuid):
    user = request.user
    friend = get_object_or_404(Users, uuid=friend_uuid)

    chat = ChatRoom.objects.create()
    chat.participants.add(user, friend)

    chat.save()
    return redirect('suggested_users')


@login_required
def chat_home(request):
    chats = ChatRoom.objects.filter(participants=request.user)
    return render(request, 'chat_app/home.html', {'chats': chats})


@login_required
def chat_view(request, chat_uuid):
    chat = get_object_or_404(ChatRoom, uuid=chat_uuid)
    chats = ChatRoom.objects.filter(participants=request.user)
    messages = Message.objects.filter(chat=chat)
    friend = Users.objects.filter(chat_rooms=chat).exclude(id=request.user.id).first()
    context = {
        'chat': chat,
        'friend': friend,
        'messages': messages,
        'chats': chats
    }
    return render(request, 'chat_app/chat.html', context)


@login_required
def get_chatted_users(request):
    # Get all chat rooms that the current user is a part of
    chats = ChatRoom.objects.filter(participants=request.user)

    return render(request, 'chat_app/friends.html', {'chats': chats})
