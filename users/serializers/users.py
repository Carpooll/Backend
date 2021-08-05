from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.models import User
from users.models import Profile, Passenger, Driver, Car

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name','last_name']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id','phone','balance', 'street', 'suburb', 'postal_code', 'internal_number', 'external_number', 'coordinate_x', 'coordinate_y']

class EditProfileSerializer(serializers.ModelSerializer):
    
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        
        profile = instance.profile

        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        
        instance.save()
        if (profile_data.get('balance', profile.balance) != None):
            profile.balance = profile_data.get('balance', profile.balance )
            
        if (profile_data.get('street', profile.street) != None and profile_data.get('street', profile.street) != ""):
            profile.street = profile_data.get('street', profile.street)

        if (profile_data.get('suburb', profile.suburb) != None and profile_data.get('suburb', profile.suburb) != ""):
            profile.suburb = profile_data.get('suburb', profile.suburb)

        if (profile_data.get('phone', profile.phone) != None and profile_data.get('phone', profile.phone) != ""):
            profile.phone = profile_data.get('phone', profile.phone)

        if (profile_data.get('postal_code', profile.postal_code) != None):
            profile.postal_code = profile_data.get('postal_code', profile.postal_code)

        if (profile_data.get('internal_number', profile.internal_number) != None):
            profile.internal_number = profile_data.get('internal_number', profile.internal_number)

        if (profile_data.get('external_number', profile.external_number) != None):
            profile.external_number = profile_data.get('external_number', profile.external_number)

        if (profile_data.get('coordinate_y', profile.coordinate_y) != None):
            profile.coordinate_y = profile_data.get('coordinate_y', profile.coordinate_y)

        if (profile_data.get('coordinate_x', profile.coordinate_x) != None):
            profile.coordinate_x = profile_data.get('coordinate_x', profile.coordinate_x)

        profile.save()

        return instance


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        
        profile = instance.profile

        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        
        instance.save()
        if (profile_data.get('balance', profile.balance) != None):
            profile.balance = profile_data.get('balance', profile.balance )
            
        if (profile_data.get('street', profile.street) != None and profile_data.get('street', profile.street) != ""):
            profile.street = profile_data.get('street', profile.street)

        if (profile_data.get('suburb', profile.suburb) != None and profile_data.get('suburb', profile.suburb) != ""):
            profile.suburb = profile_data.get('suburb', profile.suburb)

        if (profile_data.get('phone', profile.phone) != None and profile_data.get('phone', profile.phone) != ""):
            profile.phone = profile_data.get('phone', profile.phone)

        if (profile_data.get('postal_code', profile.postal_code) != None):
            profile.postal_code = profile_data.get('postal_code', profile.postal_code)

        if (profile_data.get('internal_number', profile.internal_number) != None):
            profile.internal_number = profile_data.get('internal_number', profile.internal_number)

        if (profile_data.get('external_number', profile.external_number) != None):
            profile.external_number = profile_data.get('external_number', profile.external_number)

        if (profile_data.get('coordinate_y', profile.coordinate_y) != None):
            profile.coordinate_y = profile_data.get('coordinate_y', profile.coordinate_y)

        if (profile_data.get('coordinate_x', profile.coordinate_x) != None):
            profile.coordinate_x = profile_data.get('coordinate_x', profile.coordinate_x)

        profile.save()

        return instance

class ProfileSerializerPlus(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ['id','user','phone','balance', 'street', 'suburb', 'postal_code', 'internal_number', 'external_number', 'coordinate_x', 'coordinate_y']


class PassengerSerializer(serializers.ModelSerializer):
    profile = ProfileSerializerPlus()

    class Meta:
        model = Passenger
        fields=['profile','driver']

class DriverSerializer(serializers.ModelSerializer):
    
    profile = ProfileSerializerPlus()
    class Meta:
        model = Driver
        fields=['profile']

    def update(self, instance, validated_data):

        instance.card_owner = validated_data.get('card_owner', instance.card_owner)
        instance.card_number = validated_data.get('card_number', instance.card_number)
        instance.exp_date = validated_data.get('exp_date', instance.exp_date)
        instance.ccv = validated_data.get('ccv', instance.ccv)
        instance.save()
        return instance

class DriverPrivSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Driver
        fields=['card_owner', 'card_number', 'ccv', 'exp_date']

    def update(self, instance, validated_data):

        instance.card_owner = validated_data.get('card_owner', instance.card_owner)
        instance.card_number = validated_data.get('card_number', instance.card_number)
        instance.exp_date = validated_data.get('exp_date', instance.exp_date)
        instance.ccv = validated_data.get('ccv', instance.ccv)
        instance.save()
        return instance


class CarSerializer(serializers.ModelSerializer):

    """ driver = DriverSerializer() """

    class Meta:
        model=Car
        fields=['model', 'color', 'plates', 'insurance', 'limit', 'travel_cost']

    def update(self, instance, validated_data):

        instance.model = validated_data.get('model', instance.model)
        instance.color = validated_data.get('color', instance.color)
        instance.plates = validated_data.get('plates', instance.plates)
        instance.travel_cost = validated_data.get('travel_cost', instance.travel_cost)
        instance.insurance = validated_data.get('insurance', instance.insurance)
        instance.limit = validated_data.get('limit', instance.limit)
        instance.save()
        return instance