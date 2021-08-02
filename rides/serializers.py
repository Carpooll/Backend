#rest_framework
from rest_framework import serializers
#models
from users.models import Driver, Profile, Passenger
from django.contrib.auth.models import User
from rides.models import Ride
class RideSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ride
        fields = '__all__'