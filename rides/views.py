from django.shortcuts import render
#rest_framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, mixins, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
#models
from rides.models import Ride
from users.models import Driver, Passenger
from notifications.models import RideNotification
#serializers
from rides.serializers import RideSerializer
from notifications.serializers.notifications import NotificationSerializer
#permissions
from rest_framework.permissions import IsAuthenticated

# Create your views here
class createRideViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin):
    queryset = Ride.objects.all()

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