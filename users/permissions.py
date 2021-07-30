"""user can edit permissions"""

#Django rest_framework
from rest_framework.permissions import BasePermission

#models_module
from django.contrib.auth.models import User
from users.models import Profile, Driver

from notifications.models import Notification

class IsOwnProfile(BasePermission):
    '''check if is owner'''
    def has_object_permission(self, request, view, obj):
        path = request.path.split('/')
        user_id = int(path[2])
        
        try:
            user = User.objects.get(username=request.user.username)
            print(user)
            if request.user.id == user_id:
                return True
        except user.DoesNotExist:
            return False

class IsDriver(BasePermission):
    '''check if is driver'''
    def has_object_permission(self, request, view, obj):
        profile = request.user.profile
        try:
            driver = Driver.objects.get(profile=profile)
            return True
        except Driver.DoesNotExist:
            return False

        
class IsPassenger(BasePermission):
    '''check if is driver'''
    def has_object_permission(self, request, view, obj):
        profile = request.user.profile
        try:
            passenger = Passenger.objects.get(profile=profile)
            return True
        except Passenger.DoesNotExist:
            return False

class NotificationOwnerPermission(BasePermission):
    '''check if is owner of the notification'''
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


class IsOwnProfileDriver(BasePermission):
    '''Intento de hacerlo con profile, en el view se tiene que hacer tambien con el profile si no no funciona'''
    # def has_object_permission(self, request, view, obj):
    #     path = request.path.split('/')
    #     profile_id = int(path[2])
    #     print(profile_id)
        
    #     profile = request.user.profile

    #     try:
    #         #user = User.objects.get(username=request.user.username)
    #         #driver_profile = Profile.objects.get(id=profile)
    #         print(profile.id)
    #         if profile_id == profile.id:
    #             return True
    #     except profile.DoesNotExist:
    #         return False

    def has_object_permission(self, request, view, obj):
        path = request.path.split('/')
        driver_id_path = int(path[2])
        #print(driver_id_path)

        try:
            profile_driver = Driver.objects.get(profile=request.user.profile)

            #print(profile_driver.id)
            if profile_driver.id == driver_id_path:

                return True
        except profile_driver.DoesNotExist:
            return False