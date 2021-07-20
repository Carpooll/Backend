#django
from django.contrib.auth import settings
#rest_framework
from rest_framework import serializers
#models
from django.contrib.auth.models import User
#utils
import jwt

class UserVerifiedSerializer(serializers.Serializer):
    """account verifications"""
    token = serializers.CharField()

    def validate_token(self, data):
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError({'Error':'invalid token'})
        except jwt.PyJWKError:
            raise serializers.ValidationError({'Error':'invalid token'})

        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError({'Error':'Invalid token'})
             
        self.context['payload'] = payload

        return data

    def save(self):
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.profile.is_verified = True
        user.profile.save()
        return user