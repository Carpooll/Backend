from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.models import User
from users.models import Passenger, Driver, Profile
from rides.models import Ride

class RideSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ride
        fields= "__all__"
