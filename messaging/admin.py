from django.contrib import admin
from .models import Conversation, Message

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'participant_list', 'created_at')

    def participant_list(self, obj):
        return ', '.join(p.email for p in obj.participants.all())
    participant_list.short_description = 'Participants'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'conversation', 'content_preview', 'is_read', 'created_at')

    def content_preview(self, obj):
        return obj.content[:60]
    content_preview.short_description = 'Content'