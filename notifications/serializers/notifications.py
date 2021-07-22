#rest_framework
from rest_framework import serializers
#models
from users.models import Driver, Profile, Passenger
from django.contrib.auth.models import User
from notifications.models import Notification, Request

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ['title','text', 'sendee','sender','date']