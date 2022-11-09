from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.decorators import login_required
from .models import Chat


@login_required(login_url="/api-auth/login")
def index(request):
    user = request.user
    chat_rooms = Chat.objects.filter(member=user)
    context = {"chat_rooms": chat_rooms}
    return render(request, "chat/index.html", context)


@login_required(login_url="/api-auth/login")
def room(request, room_name):
    username = request.user.username

    return render(request, "chat/room.html", {
        "room_name": room_name,
        "username": mark_safe(json.dumps(username)),
        })
