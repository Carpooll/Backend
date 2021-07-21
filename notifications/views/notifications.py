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
    serializer = ResquestDriverSerializer()
    serializer.create(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save() 
    data = {
        "message":"ahuevo"
    }
    return Response(data=data, status=status.HTTP_200_OK)