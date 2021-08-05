from users.models import Driver, Profile
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers.login import UserLoginSerializer
from users.serializers.users import UserSerializer
from users.models import Driver, Passenger


class UserLoginAPIView(APIView):

    def post(self, request, *args, **kwargs):
        """handle http POST request"""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        flag = None
        try:
            is_driver = Driver.objects.get(profile = Profile.objects.get(user=user))
            flag = True
        except:
            flag= False

        data = {
            'user': UserSerializer(user).data,
            'driver': flag,
            'token': token
        }

        return Response(data, status=status.HTTP_201_CREATED)