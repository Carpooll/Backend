"""user can edit permissions"""

#Django rest_framework
from rest_framework.permissions import BasePermission

#models_module
from django.contrib.auth.models import User
from users.models import Profile, Passenger, Driver
from notifications.models import Notification

class IsOwnProfile(BasePermission):
    '''checks if is owner'''
    def has_object_permission(self, request, view, obj):
        path = request.path.split('/')
        user_id = int(path[2])
        
        try:
            if request.user.profile.id == user_id:
                return True
        except user.DoesNotExist:
            return False

class IsDriver(BasePermission):
    '''checks if is driver'''
    def has_object_permission(self, request, view, obj):
        
        try:
            driver = Driver.objects.get(profile=request.user.profile)
            return True
        except Driver.DoesNotExist:
            return False

        
class IsPassenger(BasePermission):
    '''checks if is passenger'''
    def has_object_permission(self, request, view, obj):
        profile = request.user.profile
        try:
            passenger = Passenger.objects.get(profile=profile)

            return True
        except Passenger.IsNotFound:
            return False

class NotificationOwnerPermission(BasePermission):
    '''checks if is owner of the notification'''
    def has_object_permission(self, request,view, obj):
        path = request.path.split('/')
        notification_id = int(path[2])
               
        profile_id = request.user.profile.id
        
        notification = Notification.objects.get(id = notification_id)
        sendee = notification.sendee.id

        try:
            if (sendee == profile_id):
                return True
        except Notification.NotificationOwnerPermission:
            return False

class HasDriver(BasePermission):
    '''checks if the passenger already has a driver'''
    def has_object_permission(self, request,view, obj):
        try:
            passenger = Passenger.objects.get(profile=request.user.profile)
            if (passenger.driver == None):
                return True
        except Passenger.DoesNotExist():
            return False

class HasCar(BasePermission):

    def has_object_permission(self, request, *args, **kwargs):
        driver = Driver.objects.get(profile=request.user.profile)
        try:
            if driver != None:
                return True
        except:
            return False