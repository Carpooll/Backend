from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.models import User
from users.models import Profile

class NewUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields=['username']