from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.models import User
from users.models import Profile

""" class NewUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields=['id'] """

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id','username','first_name','last_name', 'profile']

    def update(self, instance, validated_data):
        profile = instance.profile
        print(instance)
        profile_data = validated_data.pop('profile')

        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        
        instance.save()

        profile.street = profile_data.get('street', profile.street)
        profile.suburb = profile_data.get('suburb', profile.suburb)
        profile.phone = profile_data.get('phone', profile.phone)
        profile.postal_code = profile_data.get('postal_code', profile.postal_code)
        profile.internal_number = profile_data.get('internal_number', profile.internal_number)
        profile.external_number = profile_data.get('external_number', profile.external_number)
        profile.coordinate_x = profile_data.get('coordinate_x', profile.coordinate_x)
        profile.coordinate_y = profile_data.get('coordinate_y', profile.coordinate_y)
        profile.save()

        return instance

