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
from users.permissions import NotificationOwnerPermission
from rest_framework.permissions import IsAuthenticated


class RequestNotificationViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Notification.objects.all()
    serializer_class =  NotificationSerializer
    permissions = []
    def get_permissions(self):
        permissions = []
        if self.action in ['update', 'partial_update']:
            permissions.append(NotificationOwnerPermission)
        
        return [permission() for permission in permissions]

    def create(self, request, *args, **kwargs):
        user_id = int(request.user.id)
        user = User.objects.get(id = user_id)
        profile = Profile.objects.get(user = user)
        profile_id = profile.id
        info = request.data
        data = {
            'title':info['title'],
            'text':info['text'],
            'sendee':info['sendee'],
            'sender':profile_id
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        notification = self.perform_create(serializer)
        notification1 = Request.objects.create(
            notification=notification,
        )
        headers = self.get_success_headers(serializer.data)
        data = {
            'status' : notification1.status,
            'notification id' : notification.id,
            'sendee' : info['sendee'],
            'sender' : profile_id
        }
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)\

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        requestNotification = Request.objects.get(notification = instance)
        response = request.data['status']
        requestNotification.status = response
        requestNotification.save()
        ''' getting the notification element from the request'''
        notification = requestNotification.notification

        driver = User.objects.get(Profile.id == notification.sendee.id)
        # passenger = Profile.objects.get(id  = notification.sender.id)
        print(driver)
        print(passenger)

        if requestNotification.status == 'accept':

            
            passenger.driver = Driver.objects.get(profile == driver)
            passenger.save()
        
        notification.sendee = passenger
        notification.sender = driver
        notification.save()

        return Response(requestNotification.status, status=status.HTTP_201_CREATED)\

    def perform_create(self, serializer):
        return serializer.save()

"""     def list(self,request,*args,**kwargs):
        
        queryset = Notification.objects.filter(sendee = request.user.id) 
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = NotificationSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = NotificationSerializer(queryset, many=True)
        return Response(serializer.data) """

@api_view(['POST'])
def RequestDriver(request):
    print(request.data)
    data = request.data
    serializer = RequestDriverSerializer(data=data)
    serializer.is_valid()
    notification = serializer.save()
    return Response(data=notification, status=status.HTTP_200_OK)