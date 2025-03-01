# 
# Web Socket App Set Up

### Setup and Installation
1. Install Channels:
    ```bash
    pip install channels
    ```

- ### [ASGI Configuration](#asgi-configuration)
    - [Consumers](#consumers)
    - [Routing](#routing)
- ### [Database for WebSocket](#database-for-websocket)


### ASGI Configuration
1. **asgi.py:**
    ```python
    import os
    from django.core.asgi import get_asgi_application
    from channels.routing import ProtocolTypeRouter, URLRouter
    from channels.auth import AuthMiddlewareStack
    import WebSocketApp.routing

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OAuthWebSocket.settings')

    application = ProtocolTypeRouter({
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                WebSocketApp.routing.websocket_urlpatterns
            )
        ),
    })
    ```

### Consumers
1. **consumers.py:**
    ```python
    import json
    from channels.db import database_sync_to_async
    from channels.generic.websocket import AsyncWebsocketConsumer
    from django.contrib.auth.models import User
    from datetime import datetime, timezone  # Import datetime and timezone
    from .models import ChatRoom, ChatMessage, RoomGroup

    class ChatConsumer(AsyncWebsocketConsumer):
        async def connect(self):
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = f'chat_{self.room_name}'

            # Create or get chat room
            self.room = await self.get_or_create_room(self.room_name)

            # Join room group
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

            # Add user to room group
            self.username = await self.get_name()
            await self.add_user_to_group()

            # Load old chat messages and send to the user
            old_messages = await self.get_old_messages()
            for message in old_messages:
                await self.send(text_data=json.dumps({
                    'message': f'{message["username"]}: {message["message"]}'
                }))

            # Notify room group that the user has joined
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': f'{self.username} has joined the chat.'
                }
            )

        async def disconnect(self, close_code):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

            # Remove user from room group
            if hasattr(self, 'username'):
                await self.remove_user_from_group()

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': f'{self.username} has left the chat.'
                    }
                )

        async def receive(self, text_data):
            text_data_json = json.loads(text_data)
            message = text_data_json['message']

            await self.save_message(message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': f'{self.username}: {message}'
                }
            )

        async def chat_message(self, event):
            message = event['message']
            await self.send(text_data=json.dumps({'message': message}))

        @database_sync_to_async
        def get_name(self):
            return User.objects.all()[0].username  # Replace with appropriate logic

        @database_sync_to_async
        def save_message(self, message):
            user = User.objects.get(username=self.username)
            ChatMessage.objects.create(user=user, room=self.room, message=message)

        @database_sync_to_async
        def get_or_create_room(self, room_name):
            return ChatRoom.objects.get_or_create(name=room_name)[0]

        @database_sync_to_async
        def add_user_to_group(self):
            user = User.objects.get(username=self.username)
            RoomGroup.objects.create(room=self.room, user=user)

        @database_sync_to_async
        def remove_user_from_group(self):
            user = User.objects.get(username=self.username)
            RoomGroup.objects.filter(room=self.room, user=user, left_at__isnull=True).update(left_at=datetime.now(timezone.utc))

        @database_sync_to_async
        def get_old_messages(self):
            messages = ChatMessage.objects.filter(room=self.room).order_by('timestamp')
            return [{'username': message.user.username, 'message': message.message} for message in messages]
    ```

### Routing
1. **routing.py:**
    ```python
    from django.urls import re_path
    from . import consumers

    websocket_urlpatterns = [
        re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    ]
    ```

## Database for WebSocket
Ensure your models are set up to store chat messages and room group data.

**models.py:**
```python
from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class RoomGroup(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    left
