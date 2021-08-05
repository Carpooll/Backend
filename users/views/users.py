#rest_framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, mixins, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
#models
from django.contrib.auth.models import User
from users.models import Profile, Passenger, Driver, Car
#serializers
from users.serializers.is_passenger import IsPassenger
#from users.serializers.users import NewUserSerializer
from users.serializers.signup import UserSignupSerializer
from users.serializers.users import UserSerializer, PassengerSerializer, DriverSerializer, CarSerializer, DriverPrivSerializer, EditProfileSerializer
from users.serializers.verified import UserVerifiedSerializer


#permissions
from users.permissions import IsOwnProfile, IsDriver, IsPassenger, HasCar
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
        data = {'token':f'{token}'}
        serializer = UserVerifiedSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message':'account verified successfully'}
        return Response(data, status=status.HTTP_200_OK) 
        

@api_view(['POST'])
def is_passenger(request):
    if request.method == 'POST':
        serializer = IsPassenger(data=request.data)
        serializer.create(data=request.data)
        return Response(request.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def available_drivers(request):
    if request.method == 'GET':
        data = Driver.objects.all()
        print(data)
        drivers = []
        for driver in data:
            if driver.car.limit>0:

                drivers.append({
                    "profile_id" : driver.profile.id,
                    "phone": driver.profile.phone,
                    "First_name" : driver.profile.user.first_name,
                    "Last_name" : driver.profile.user.last_name,
                    "Travel_cost" : driver.car.travel_cost,
                    "Limit": driver.car.limit,
                    "Coordinate_x" : driver.profile.coordinate_x,
                    "Coordinate_y" : driver.profile.coordinate_y,
                })
        print(drivers)
        # serializer = DriverSerializer(data=drivers)
        # serializer.is_valid(data=drivers)
        return Response(drivers, status=status.HTTP_200_OK)

class PassengerListView(ListAPIView):
    '''list all users'''
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

class DriverListView(ListAPIView):
    '''list driver's passengers'''

    # def get(request, *args, **kwargs):
    #     driverId = request.user.profile.id

    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

""" class DriversPassengers(ListAPIView):
    '''listing the passengers of each driver'''
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
 """

class DriverPassengersViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class =  PassengerSerializer
    permissions = []

    def list(self, request, *args, **kwargs):
        driver = request.user.profile.id
        queryset = self.filter_queryset(Passenger.objects.filter(driver=driver))

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class PassengerDriver(viewsets.GenericViewSet, mixins.RetrieveModelMixin):

    serializer_class =  DriverSerializer
    permissions = [IsPassenger]


    def list(self, request, *args, **kwargs):
    
        passenger = Passenger.objects.get(profile=request.user.profile)
        print(request.user.profile)
        driver_id = passenger.driver.id
        driver = Profile.objects.get(id=driver_id)
        print(driver.user.username)
        queryset = self.filter_queryset(Driver.objects.filter(profile=driver))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data) 

class ProfileCompletionViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = EditProfileSerializer
    permission_classes=[IsOwnProfile]

class ProfileEditViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes=[]

class CarViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permissions = []
    def create(self, request, *args, **kwargs):
        
        driver = Driver.objects.get(profile=request.user.profile)
        if(driver.car != None):
            response = {
            "error":"car already exists, try update method instead",
            "id":f"{driver.car.id}"
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        car = Car.objects.create(
            color = request.data['color'],
            model = request.data['model'],
            plates = request.data['plates'],
            insurance = request.data['insurance'],
            limit = request.data['limit'],
            travel_cost = request.data['travel_cost'])

        driver.car = car
        driver.save()
        response = {
            "message":"success",
            "id":f"{car.id}"
        }
        return Response(response, status=status.HTTP_201_CREATED)
        
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = Car.objects.get(driver=Driver.objects.get(profile=request.user.profile))
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class PaymentViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    queryset = Driver.objects.all()
    serializer_class = DriverPrivSerializer
    permission_classes=[IsOwnProfile]

    def retrieve(self, request, *args, **kwargs):
        id = request.path.split('/')
        id=int(id[3])
        instance = Driver.objects.get(profile = Profile.objects.get(id=id))

        if instance.profile == request.user.profile:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        id = request.path.split('/')
        id=int(id[3])
        if id == request.user.profile.id:
            instance = Driver.objects.get(profile=Profile.objects.get(id=id))
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            data = {
                "error":"you dont have permission to perform this action"
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
