#rest_framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, mixins, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
#models
from django.contrib.auth.models import User
from users.models import Profile, Passenger, Driver
from notifications.models import Request, Notification, RideNotification
from rides.models import Ride as RideModel
#serializers
from notifications.serializers.notifications import NotificationSerializer
#permissions
from users.permissions import NotificationOwnerPermission, HasDriver
from rest_framework.permissions import IsAuthenticated

class RideNotificationViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    queryset = Notification.objects.all()
    serializer_class =  NotificationSerializer
    permissions = []

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        rideNotification = RideNotification.objects.get(notification = instance)
        response = request.data['status']
        rideNotification.status = response
        rideNotification.save()
        ''' getting the notification element from the request'''
        notification = rideNotification.notification

        print(rideNotification.ride_id)
        travel = RideModel.objects.get(id=rideNotification.ride_id)
        if travel.is_active:
            if travel.passenger1 == None:
                travel.passenger1 = request.user.profile.id
            elif travel.passenger2 == None:
                travel.passenger2 = request.user.profile.id
            elif travel.passenger3 == None:
                travel.passenger3 = request.user.profile.id
            elif travel.passenger4 == None:
                travel.passenger4 = request.user.profile.id
            elif travel.passenger5 == None:
                travel.passenger5 = request.user.profile.id
            elif travel.passenger6 == None:
                travel.passenger6 = request.user.profile.id
            travel.save()

            data = {
                "message" : "Se acepto la solicitud"
            }

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {
                "message" : "Este viaje ya no esta disponible"
            }

            return Response(data, status=status.HTTP_403_FORBIDDEN)
            


class RequestNotificationViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Notification.objects.all()
    serializer_class =  NotificationSerializer
    permissions = []

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if(instance.sendee.id != request.user.profile.id):
            data={
                'message':'you dont have permission to delete this instance'
            }
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        else:
            data={
                'message':'succesfully deleted'
            }
            self.perform_destroy(instance)
            return Response(data,status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(Notification.objects.filter(sendee = request.user.profile.id))
        notifications = Notification.objects.filter(sendee = request.user.profile.id)
        response = []
        for notification in notifications:
            try:
                ride_notification = RideNotification.objects.get(notification=notification)
                _notification = {
                    "id":notification.id,
                    "title":notification.title,
                    "text":notification.text,
                    "sendee":notification.sendee.id,
                    "sender":notification.sender.id,
                    "date":notification.date,
                    "ride_cost":ride_notification.cost
                }
            except:
                _notification = {
                    "id":notification.id,
                    "title":notification.title,
                    "text":notification.text,
                    "sendee":notification.sendee.id,
                    "sender":notification.sender.id,
                    "date":notification.date,
                }
            
            response.append(_notification)
        response = {
            "results":response
        }
        return Response(response)


    def create(self, request, *args, **kwargs):
        user_id = int(request.user.id)
        user = User.objects.get(id = user_id)
        profile = Profile.objects.get(user = user)

        try:
            passenger=Passenger.objects.get(profile=request.user.profile)
            driver_id=passenger.driver
            if driver_id.id != None:
                data = {
                    "message": "Usted ya tiene un conductor"
                }
                return Response(data=data, status=status.HTTP_403_FORBIDDEN)
        except:
            pass

        profile_id = profile.id
        info = request.data
        data = {
            'title':info['title'],
            'text':info['text'],
            'sendee':info['sendee'],
            'sender':profile_id
        }
    
        flag = False
        passenger=Profile.objects.get(id=profile_id)
        driver=Profile.objects.get(id=info["sendee"])
        try:
            notifications=Notification.objects.filter(sender=passenger, sendee=driver)
        
            for notification in notifications:
                try:
                    request=Request.objects.get(notification=notification)
                    data = {
                        "message": "Usted ya envio una solicitud a este conductor"
                            }
                    return Response(data=data, status=status.HTTP_403_FORBIDDEN)

                except:
                    pass
        except:
            pass
       

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
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        requestNotification = Request.objects.get(notification = instance)
        response = request.data['status']
        requestNotification.status = response
        requestNotification.save()
        ''' getting the notification element from the request'''
        notification = requestNotification.notification

        driver = Profile.objects.get(id = notification.sendee.id)
        passenger = Profile.objects.get(id  = notification.sender.id)

        if requestNotification.status == 'accept': 
            driver = Profile.objects.get(id = notification.sendee.id)
            passenger = Profile.objects.get(id = notification.sender.id)
            passenger = Passenger.objects.get(profile=passenger)
            driver = Profile.objects.get(id = notification.sendee.id)
            _driver = Driver.objects.get(profile=driver)
            if _driver.car.limit<1:
                message = {
                    "message":"you dont have any available spaces in your car!",
                }
                return Response(message, status=status.HTTP_403_FORBIDDEN)
            
            if passenger.driver != None:
                message = {
                    "message":"This passenger already has a driver",
                }
                return Response(message, status=status.HTTP_403_FORBIDDEN)
            passenger.driver = driver
            print("simonki")
            passenger.save()
            _driver.car.limit = _driver.car.limit - 1
            _driver.car.save()
            
            notification.title = "the request was accepted"
            notification.text = "The driver accepted to give you a ride"
            data = {
            "message" : "Se acepto la solicitud"
            }
            notification.sendee = Profile.objects.get(id = passenger.profile.id)
            notification.sender = Profile.objects.get(id = driver.id)
        else:
            driver = Profile.objects.get(id = notification.sendee.id)
            passenger = Profile.objects.get(id  = notification.sender.id)
            notification.title = "the request was rejected"
            notification.text = "The driver rejected to give you a ride"
            data = {
            "message" : "Se rechazo la solicitud"
            }
            notification.sendee = Profile.objects.get(id = passenger.id)
            notification.sender = Profile.objects.get(id = driver.id)
        
        notification.save()

        return Response(data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save()
        
@api_view(['POST'])
def RequestDriver(request):
    print(request.data)
    data = request.data
    serializer = RequestDriverSerializer(data=data)
    serializer.is_valid()
    notification = serializer.save()
    return Response(data=notification, status=status.HTTP_200_OK)