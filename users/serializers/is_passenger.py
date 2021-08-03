from users.models import Profile, Passenger
from rest_framework import serializers
from django.contrib.auth.models import User

class IsPassenger(serializers.Serializer):

    def create(self, data):
        user = User.objects.get(id=data['id'])
        profile = Profile.objects.get(user=user)
        passenger = Passenger(profile = profile) 
        
        passenger.save()

        return passenger