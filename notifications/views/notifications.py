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
#serializers
from notifications.serializers.notifications import NotificationSerializer
#permissions
from users.permissions import IsOwnProfile
from rest_framework.permissions import IsAuthenticated


class RequestNotificationViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Notification.objects.all()
    serializer_class =  NotificationSerializer
    permissions = []

    def create(self, request, *args, **kwargs):
        user_id = int(request.user.id)
        print(user_id)
        info = request.data
        data = {
            'title':info['title'],
            'text':info['text'],
            'sendee':info['sendee'],
            'sender':user_id
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        notification = serializer.save()

    def list(self,request,*args,**kwargs):
        """list all post data with authors"""
        
        queryset = Notification.objects.filter(sendee = request.user.id) 
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = NotificationSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = NotificationSerializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def RequestDriver(request):
    print(request.data)
    data = request.data
    serializer = RequestDriverSerializer(data=data)
    serializer.is_valid()
    notification = serializer.save()
    return Response(data=notification, status=status.HTTP_200_OK)