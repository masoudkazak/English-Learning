from enum import unique
from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    roomname = models.CharField(max_length=50, unique=True)
    member = models.ManyToManyField(User, null=True, blank=True)

    def __str__(self):
        return self.roomname


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    related_chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def last_message(self, roomname):
        return Message.objects.filter(related_chat__roomname=roomname).order_by("-timestamp")
    
    def __str__(self):
        return self.author.username
