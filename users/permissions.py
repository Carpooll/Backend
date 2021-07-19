"""user can edit permissions"""

#Django rest_framework
from rest_framework.permissions import BasePermission

#models_module
from django.contrib.auth.models import User
from users.models import Profile

class IsOwnProfile(BasePermission):
    '''check if is owner'''
    def has_object_permission(self, request, view, obj):
        path = request.path.split('/')
        user_id = int(path[2])

        try:
            user = User.objects.get(username=request.user.username)
            if request.user.id == user_id:
                return True
        except user.DoesNotExist:
            return False
