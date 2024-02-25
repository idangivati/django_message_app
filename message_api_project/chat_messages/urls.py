from django.urls import path
from .views import *

urlpatterns = [
    path('chat_messages/', MessageListCreateAPIView.as_view(), name='message-list-create'),
    path('create-user/', CreateUserAPIView.as_view(), name='create-user'),
    path('unread-messages/', UnreadMessageListAPIView.as_view(), name='unread-messages'),
    path('read_message/', ReadMessageAPIView.as_view(), name='read_message'),
    path('delete_message/<int:pk>/', DeleteMessageAPIView.as_view(), name='delete-message'),
    path('read_all/', ReceiveAllMessages.as_view(), name='read_all')
]
