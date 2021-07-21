#rest_framework
from rest_framework import serializers
#models
from users.models import Driver, Profile, Passenger
from django.contrib.auth.models import User
from notifications.models import Notification, Request

from notifications.serializers.notification import NotificationSerializer

class ResquestDriverSerializer(serializers.Serializer):
    def create(self, data):
        print()
        try:
            driver = Profile.objects.get(user_id=data['driver'])
        except Driver.DoesNotExist:
            raise serializers.ValidationError({'error':'driver not found'})
        try:
            passenger = Profile.objects.get(id=data['passenger'])
        except Passenger.DoesNotExist:
            raise serializers.ValidationError({'error':'passenger not found'})
        name = User.objects.get(profile=passenger)
        name = name.first_name
        data = {
            "title":f"{name} wants to travel with you",
            "text":"jalas o te cagas",
            "sendee":f"{driver.id}",
            "sender":f"{passenger.id}",
        }
        serializer = NotificationSerializer(data=data)
        serializer.create()
