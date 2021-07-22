"""user can edit permissions"""

#Django rest_framework
from rest_framework.permissions import BasePermission

#models_module
from django.contrib.auth.models import User
from users.models import Profile

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

class NotificationOwnerPermission(BasePermission):
    '''check if is owner of the notification'''
    def has_object_permission(self, request,view, obj):
        path = request.path.split('/')
        notification_id = int(path[2])
        
        user_id = request.user.id
        profile = Profile.objects.get(user.id == user_id)
        profile_id = profile.id

        notification = Notification.objects.get(id = notification_id)
        try:
            if (notification.sendee.id == profile_id):
                return True
        except Notification.NotificationOwnerPermission:
            return False