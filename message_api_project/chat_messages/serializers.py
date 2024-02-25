from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    creation_date_format = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['pk', 'sender', 'receiver', 'subject', 'message', 'creation_date_format', 'is_read']

    def get_creation_date_format(self, obj):
        # Customize the display format of the creation date
        return obj.creation_date.strftime("%Y-%m-%d %H:%M:%S %Z")

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value
