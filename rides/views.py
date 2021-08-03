from django.shortcuts import render
#rest_framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, mixins, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
#models
from rides.models import Ride
from users.models import Driver
#serializers
from rides.serializers import RideSerializer
#permissions
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class createRideViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):

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
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
