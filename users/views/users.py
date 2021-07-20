#rest_framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, mixins, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
#models
from django.contrib.auth.models import User
from users.models import Profile
#serializers
#from users.serializers.users import NewUserSerializer
from users.serializers.signup import UserSignupSerializer
from users.serializers.users import UserSerializer
from users.serializers.verified import UserVerifiedSerializer
#permissions
from users.permissions import IsOwnProfile
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        #data = NewUserSerializer(user).data
        return Response(user)

@api_view(['GET'])
def args_demo(request, si):
    if request.method == 'GET':
        demo = request.path.split('/')
        
        data = {'message':f'{demo[3]}'}
        return Response(data)

@api_view(['GET'])
def account_verification(request, token):
    if request.method == 'GET':
        token = request.path.split('/')
        token = token[3]
        """data = {'token':f'{token}'}
        return Response(data) """
        data = {'token':f'{token}'}
        serializer = UserVerifiedSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message':'accouont verified successfully'}
        return Response(data, status=status.HTTP_200_OK) 
        
class ProfileCompletionViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes=[IsOwnProfile]

class ProfileEditViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes=[]

    