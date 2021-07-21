#rest_framework
from rest_framework import serializers
#models
from users.models import Driver
from django.contrib.auth.models import User
from notifications.models import Notification, Request

class NotificationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50)

    text = serializers.CharField(max_length=150)

    sendee = serializers.IntegerField()
    
    sender = serializers.IntegerField()

    def create(self, data):
        sendee = User.objects.get(id = data[sendee])
        sender = User.objects.get(id = data[sender])
        notification = Notification(
            title=data['title'], 
            text=data['text'], 
            sendee=sendee
        )
        notification.save()
        request = Request(
            notification=notification,
            sender = sender
        )
        request.save()