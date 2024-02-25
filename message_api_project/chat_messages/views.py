from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Message
from .serializers import MessageSerializer
from django.contrib.auth.models import User


class BaseMessageAPIView:
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]


class DeleteMessageAPIView(BaseMessageAPIView, generics.DestroyAPIView):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user == instance.sender or request.user == instance.receiver:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "You do not have permission to delete this message."},
                            status=status.HTTP_403_FORBIDDEN)


class ReceiveAllMessages(BaseMessageAPIView, generics.ListAPIView):
    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user)


class ReadMessageAPIView(BaseMessageAPIView, generics.RetrieveAPIView):
    def get_object(self):
        unread_message = Message.objects.filter(receiver=self.request.user, is_read=False).first()
        if unread_message:
            unread_message.is_read = True
            unread_message.save()
            return unread_message
        else:
            return Message.objects.filter(receiver=self.request.user).order_by('creation_date').last()

    def get_queryset(self):
        queryset = Message.objects.filter(receiver=self.request.user)
        queryset.update(is_read=True)
        return queryset


class CreateUserAPIView(APIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.is_staff:
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')

            if not (username and email and password):
                return Response({"error": "Please provide username, email, and password"},
                                status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(username=username, email=email, password=password)
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        else:
            # User is not authenticated or is not an admin
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)


class MessageListCreateAPIView(BaseMessageAPIView, generics.ListCreateAPIView):
    def has_permission(self, request):
        if request.method == 'POST':
            return True
        return request.user and request.user.is_staff

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class UnreadMessageListAPIView(BaseMessageAPIView, generics.ListAPIView):
    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user, is_read=False)
