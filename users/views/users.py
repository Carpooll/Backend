#rest_framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, mixins, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
#models
from django.contrib.auth.models import User
from users.models import Profile, Passenger, Driver
#serializers
from users.serializers.is_passenger import IsPassenger
#from users.serializers.users import NewUserSerializer
from users.serializers.signup import UserSignupSerializer
from users.serializers.users import UserSerializer, PassengerSerializer, DriverSerializer
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
        

@api_view(['POST'])
def is_passenger(request):
    if request.method == 'POST':
        serializer = IsPassenger(data=request.data)
        serializer.create(data=request.data)
        return Response(request.data, status=status.HTTP_200_OK)

class PassengerListView(ListAPIView):
    '''list all users'''
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

class DriverListView(ListAPIView):
    '''list all users'''
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

class ProfileCompletionViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes=[IsOwnProfile]

class ProfileEditViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes=[]
