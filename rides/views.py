from django.shortcuts import render
#rest_framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, mixins, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
#models
from rides.models import Ride
from users.models import Driver, Passenger, Profile
from notifications.models import RideNotification
#serializers
from rides.serializers import RideSerializer
from notifications.serializers.notifications import NotificationSerializer
#permissions
from rest_framework.permissions import IsAuthenticated
from bson import json_util

import uuid
from datetime import datetime


from flask_pymongo import pymongo
from dotenv import load_dotenv
load_dotenv()

import os

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
client = pymongo.MongoClient(f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@dbexample.kadqv.mongodb.net/{DB_NAME}?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
db = client.iot


# Create your views here
class createRideViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    def sendNotifications(self, driver_id, cost, ride_id):

        passengers = Passenger.objects.filter(driver=driver_id) # Saves all passengers

        for passenger in passengers:
            data = {
                'title': 'Your driver has begun a ride',
                'text': 'Are you going along with your driver?',
                'sendee': passenger.profile.id,
                'sender': driver_id
            }

            serializer = NotificationSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            notification = serializer.save()

            rideNotification = RideNotification.objects.create(notification=notification, cost=cost, ride_id=ride_id)
            rideNotification.save()

    def create(self, request, *args, **kwargs):
        driver_id = request.user.profile.id

        driver = Driver.objects.get(profile=request.user.profile)
        travel_cost = driver.car.travel_cost

        data = {
            'driver': request.user.profile.id,
            'cost': travel_cost
        }
        serializer = RideSerializer(data=data)
        serializer.is_valid()
        ride = serializer.save()
        ride_id = ride.id
        headers = self.get_success_headers(serializer.data)

        self.sendNotifications(driver_id, travel_cost, ride_id)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
    
        data = {
            "message" : "El viaje ha terminado"
        }

        return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
def transaction(request):
    if request.method == 'POST':

        reciver = Profile.objects.get(id=request.data['driver'])
        sender = Profile.objects.get(id=request.data['passenger'])
        amount = request.data['amount']

        _request= db.passenger_transactions.find_one({"_id":sender.user.username})
        _request_= db.passenger_transactions.find_one({"_id":reciver.user.username})
        try:
            balance = _request['current_balance']
            balance_r = _request_['current_balance']
            if balance >= amount:

                date=datetime.now()
                date_str =date.strftime('%d/%m/%Y')
                transaction_id = uuid.uuid1()
                try:
                    db.passenger_transactions.update_one(
                        {"_id": reciver.user.username},
                        {"$push":
                            {
                            "transactions":{"id": transaction_id,"date": date_str,"amount": amount}
                            }
                        }
                    )
                    db.passenger_transactions.update_one(
                        {'_id':reciver.user.username},{'$set':{'current_balance': (balance_r+amount)}})

                    
                    db.passenger_transactions.update_one(
                        {"_id": sender.user.username},
                        {"$push":
                            {
                            "transactions":{"id": transaction_id,"date": date_str,"amount": -amount}
                            }
                        }
                    )
                    db.passenger_transactions.update_one(
                        {'_id':sender.user.username},{'$set':{'current_balance': (balance-amount)}})

                    message = {
                        'message':'transaction successfully made'
                    }
                except:
                    message = {
                        'message':'transaction error'
                    }
            else:
                message = {
                    'message':'the money is not enought'
                }
        except:
            message = {
                    'message':'any money was found'
                }

        return Response(message)