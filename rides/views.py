from django.shortcuts import render

# Create your views here.
#rest_framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, mixins, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
#models
from django.contrib.auth.models import User
from users.models import Profile, Passenger, Driver
from notifications.models import Request, Notification
from rides.models import Ride
#serializers
from notifications.serializers.notifications import NotificationSerializer
from rides.serializers import RideSerializer
#permissions
from users.permissions import NotificationOwnerPermission, HasDriver
from rest_framework.permissions import IsAuthenticated

class RideViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permissions = []
    def create(self,request, *args, **kwargs):
        driver = request.user.profile
        passengers = Driver.objects.filter(driver=driver)
        cost = Driver.objects.get(profile=driver)
        cost = cost.car.travel_cost
        ride = Ride.objects.create(driver=driver, cost = cost, passengers=passengers)
        ride.save()
        