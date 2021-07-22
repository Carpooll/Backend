#rest_framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, mixins, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
#models
from django.contrib.auth.models import User
from users.models import Profile, Passenger, Driver
from notifications.models import Request
#serializers
from notifications.serializers.request_driver import ResquestDriverSerializer
#permissions
from users.permissions import IsOwnProfile
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def RequestDriver(request):
    print(request.data)
    data = request.data
    serializer = ResquestDriverSerializer(data=data)
    serializer.is_valid()
    notification = serializer.save()
    return Response(data=notification, status=status.HTTP_200_OK)