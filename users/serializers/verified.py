#django
from django.contrib.auth import settings
#rest_framework
from rest_framework import serializers
#models
from django.contrib.auth.models import User
#utils
import jwt

from flask_pymongo import pymongo
from dotenv import load_dotenv
load_dotenv()

import os

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
client = pymongo.MongoClient(f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@dbexample.kadqv.mongodb.net/{DB_NAME}?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.iot


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
        user.profile.is_verify = True
        username = user.username
        try:
            str(db.passenger_transactions.insert_one({
                    '_id': username,
                    'current_balance':0 
                }).inserted_id)
        except:
            pass
        user.profile.save()
        return user