#rest_framework
from rest_framework import serializers
#models
from users.models import Driver, Profile, Passenger
from django.contrib.auth.models import User
from notifications.models import Notification, Request

from notifications.serializers.notification import NotificationSerializer

class ResquestDriverSerializer(serializers.Serializer):
    def create(self, data):

        driver_username = str(data.get('driver'))
        passenger_username = data.get('passenger')
        driver = User.objects.get(username = "6519150032")
        print(driver)
        passenger = User.objects.get(username = data.get('driver'))
        
        print (passenger)
       
        driver = User.objects.filter(id = driver_id)
        driver = driver[0]
        
        data = {
            "title":f"{name} wants to travel with you",
            "text":"jalas o te cagas",
            "sendee":f"{driver}",
        }
        print (data)
        self.context['passenger'] = passenger
        return data

    def send(self, data):
        passenger = self.context['passenger']
        serializer = NotificationSerializer()
        notification = serializer.create(data=data)
        notification_request = Request(notification, passenger)
        
    