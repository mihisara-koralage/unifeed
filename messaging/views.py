from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()

@login_required
def inbox(request):
    # All conversations this user is part of, most recent first
    conversations = request.user.conversations.prefetch_related(
        'participants', 'messages'
    ).order_by('-created_at')

    # Attach the "other person" and "last message" to each conversation
    conv_data = []
    for conv in conversations:
        other = conv.participants.exclude(id=request.user.id).first()
        last_msg = conv.messages.last()
        unread = conv.messages.filter(is_read=False).exclude(sender=request.user).count()
        conv_data.append({
            'conversation': conv,
            'other_user': other,
            'last_message': last_msg,
            'unread_count': unread,
        })

    return render(request, 'messaging/inbox.html', {'conv_data': conv_data})


@login_required
def open_conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    if other_user == request.user:
        return redirect('messaging:inbox')

    # Get existing or create new conversation
    conversation = Conversation.get_or_create_between(request.user, other_user)

    # Mark all unread messages in this conversation as read
    conversation.messages.filter(
        is_read=False
    ).exclude(
        sender=request.user
    ).update(is_read=True)

    # Load message history
    messages = conversation.messages.select_related('sender').all()

    return render(request, 'messaging/chat.html', {
        'conversation': conversation,
        'other_user': other_user,
        'messages': messages,
    })


@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if message.sender == request.user:
        message.is_deleted_by_sender = True
        message.save()

    elif request.user in message.conversation.participants.all():
        message.is_deleted_by_recipient = True
        message.save()

    return redirect('messaging:conversation', user_id=message.conversation.participants.exclude(
        id=request.user.id
    ).first().id)