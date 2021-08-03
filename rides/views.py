from django.shortcuts import render
#rest_framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, mixins, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
#models
from rides.models import Ride
#serializers
from rides.serializers import RideSerializer
#permissions
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class createRideViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):

    def create(self, request, *args, **kwargs):
        driver_id = request.profile.id()

        driver = Driver.objects.get(profile=request.profile)
        travel_cost = driver.car.travel_cost()

        data = {
            'driver': driver,
            'cost': travel_cost
        }

        headers = self.get_success_headers(serializer.data)

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)