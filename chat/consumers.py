import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .serializers import MessageSerializer
from .models import Message, Chat
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.models import User


class ChatConsumer(WebsocketConsumer):
    def new_message(self, data):
        message = data["message"]
        author = data["username"]
        roomname = data["roomname"]

        user = User.objects.filter(username=author).first()
        
        self.create_chat_model(user, roomname)

        chat_model = Chat.objects.get(roomname=roomname)

        message_model = Message.objects.create(
            author=user,
            content=message,
            related_chat=chat_model,
        )
        result = eval(self.message_serializer(message_model))
        self.send_to_chat_message(result)
    
    def create_chat_model(self, user, roomname):
        chat = Chat.objects.filter(roomname=roomname)
        if chat.exists():
            if user not in list(chat[0].member.all()):
                chat[0].member.add(user)
        else:
            new_chat = Chat.objects.create(
                roomname=roomname
            )
            new_chat.member.add(user)

    def fetch_message(self, data):
        roomname = data["roomname"]
        qs = Message.last_message(self, roomname)
        message_json = self.message_serializer(qs)
        content = {
            "message": eval(message_json),
            "command": "fetch_message",
        }
        self.chat_message(content)

    def message_serializer(self, qs):
        serialized = MessageSerializer(
            qs,
            many=(lambda qs: True if(qs.__class__.__name__=="QuerySet") else False)(qs)
            )
        content = JSONRenderer().render(serialized.data)
        return content

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    commands = {
        "new_message": new_message,
        "fetch_message": fetch_message,
    }

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json["command"]
        self.commands[command](self, text_data_json)
    
    def send_to_chat_message(self, message):
        print(message)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "content": message["content"],
                "command": "new_message",
                "username": message["__str__"],
            }
        )
    
    def chat_message(self, event):
        self.send(text_data=json.dumps(event))
