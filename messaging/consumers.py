import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']

        # Reject unauthenticated connections immediately
        if not self.user.is_authenticated:
            await self.close()
            return

        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'

        # Verify this user actually belongs to this conversation
        is_participant = await self.check_participant()
        if not is_participant:
            await self.close()
            return

        # Join the Redis channel group for this conversation
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'chat_message':
            content = data.get('content', '').strip()
            if not content:
                return

            # Save to database
            message = await self.save_message(content)

            # Broadcast to everyone in the group (including sender)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',       # maps to the method below
                    'message_id': message.id,
                    'content': message.content,
                    'sender_email': self.user.email,
                    'sender_id': self.user.id,
                    'timestamp': message.created_at.strftime('%H:%M'),
                }
            )

        elif message_type == 'typing':
            # Broadcast typing indicator to the OTHER person only
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_indicator',
                    'sender_id': self.user.id,
                    'sender_email': self.user.email,
                    'is_typing': data.get('is_typing', False),
                }
            )

    # Called when a 'chat_message' event arrives from the channel layer
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message_id': event['message_id'],
            'content': event['content'],
            'sender_email': event['sender_email'],
            'sender_id': event['sender_id'],
            'timestamp': event['timestamp'],
        }))

    # Called when a 'typing_indicator' event arrives
    async def typing_indicator(self, event):
        # Don't send the typing indicator back to the person who is typing
        if event['sender_id'] != self.user.id:
            await self.send(text_data=json.dumps({
                'type': 'typing',
                'sender_email': event['sender_email'],
                'is_typing': event['is_typing'],
            }))

    @database_sync_to_async
    def check_participant(self):
        return Conversation.objects.filter(
            id=self.conversation_id,
            participants=self.user
        ).exists()

    @database_sync_to_async
    def save_message(self, content):
        conversation = Conversation.objects.get(id=self.conversation_id)
        return Message.objects.create(
            conversation=conversation,
            sender=self.user,
            content=content,
        )