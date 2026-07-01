from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('',               views.inbox,             name='inbox'),
    path('<int:user_id>/', views.open_conversation, name='conversation'),
    path('delete/<int:message_id>/', views.delete_message, name='delete_message'),
]