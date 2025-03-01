from datetime import datetime, timezone
import json
# from asgiref.sync import await 
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from . models import ChatRoom, ChatMessage, RoomGroup
from django.db import models
from channels.generic.websocket import AsyncWebsocketConsumer
 # Using the Asnyc web consumer 

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = f'chat_{self.room_name}'

            # fetch room or create
            self.room = await self.get_or_create_room(self.room_name)

            # Join room group
            await (self.channel_layer.group_add)( 
                self.room_group_name,
                self.channel_name)
            
            await self.accept()

            # Adding uuser to group
            self.username = await self.get_name()
            await self.add_user_to_group()

            # Load old chat messages and send to the user
            old_messages = await self.get_old_messages()
            for message in old_messages:
                await self.send(text_data=json.dumps({
                'message': f'{message["username"]}: {message["message"]}'}))
            
            # Send connection establishment message
            await self.channel_layer.group_send(
                   self.room_group_name,
                   {
                          'type':'chat_message',
                          'message':f'{self.username} has joined the chat'
                   }
            )
            # await self.send(text_data=json.dumps({
            #     'type': 'connection_established',
            #     'message': 'You are connected'
            # }))

            # Leave room group

    async def disconnect(self, close_code):
            await (self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )
            if hasattr(self,'username'):
                   await self.remove_user_from_group()

                   await self.channel_layer.group_send(
                          self.room_group_name,
                          {
                                 'type': 'chat_message',
                                 'message': f'{self.username} has left the chat'
                          }
                   )
            
        # Receive message from WebSocket
    async def receive(self, text_data):
            text_data_json = json.loads(text_data)
            message = text_data_json["message"]

            await self.save_message(message)
             # Send message to room group
            await self.channel_layer.group_send(
                   self.room_group_name,
                   {
                          'type': 'chat_message',
                          'message': f'{self.username}: {message}'
                   }
            )

        # Receive message from room group
    async def chat_message(self, event):
            message = event["message"]

            # Send message to WebSocket
            await self.send(text_data=json.dumps({'message': message}))
            
    # database operations

    @database_sync_to_async
    def get_name(self):
           return User.objects.all()[0].username
    
    @database_sync_to_async
    def save_message(self, message):
           user= User.objects.get(username=self.username)
           ChatMessage.objects.create(user=user, room=self.room, message=message)

    @database_sync_to_async
    def get_or_create_room(self, room_name):
           return ChatRoom.objects.get_or_create(name=room_name)[0]
    
    @database_sync_to_async
    def add_user_to_group(self):
           user= User.objects.get(username = self.username)
           RoomGroup.objects.create(room= self.room, user=user)

    @database_sync_to_async
    def remove_user_from_group(self): #update the left time on leaving
           user = User.objects.get(username=self.username)
           RoomGroup.objects.filter(room=self.room,user=user,left_at__isnull=True).update(left_at=datetime.now(timezone.utc))

    @database_sync_to_async
    def get_old_messages(self):
            messages = ChatMessage.objects.filter(room=self.room).order_by('timestamp')
            return [{'username': message.user.username, 'message': message.message} for message in messages]