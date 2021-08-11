#rest_framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, mixins, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
#models
from django.contrib.auth.models import User
from users.models import Profile, Passenger, Driver, Car
from rides.models import Ride
from notifications.models import RideNotification
#serializers
from users.serializers.is_passenger import IsPassenger
#from users.serializers.users import NewUserSerializer
from users.serializers.signup import UserSignupSerializer
from users.serializers.users import UserSerializer, PassengerSerializer, DriverSerializer, CarSerializer, DriverPrivSerializer, EditProfileSerializer
from users.serializers.verified import UserVerifiedSerializer
#la formula secreta de la cangreburger
from users.views.formule import get_distance

#redirect
from django.http import HttpResponseRedirect

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
        return HttpResponseRedirect("https://carpooll.github.io/Web-Front-end/#/welcome")
        

@api_view(['POST'])
def is_passenger(request):
    if request.method == 'POST':
        serializer = IsPassenger(data=request.data)
        serializer.create(data=request.data)
        return Response(request.data, status=status.HTTP_200_OK)
        
@api_view(['GET'])
def close_ride(request):
    if request.method == 'GET':
        
        try:
            rides = Ride.objects.filter(driver = request.user.profile, is_active=True)
            for ride in rides:
            
                notifications = RideNotification.objects.filter(ride_id = ride.id)
                for notification in notifications:
                    try:
                        notification.notification.delete()
                    except:
                        pass
                ride.is_active = False
                ride.save()
            response = {
                'message':'ride successfully closed'
            }
            return Response(response)
        except:
            response = {
                'message':'This driver has any active rides'
            }
            return Response(response)

@api_view(['GET'])
def driver_is_on_ride(request):
    if request.method == 'GET':
        driver = request.user.profile
        rides= Ride.objects.filter(driver=driver, is_active=True)
        response = {
                "is_active":'False'
            }
        for ride in rides:
            if(ride.is_active == True):
                response = {
                    "is_active":'True'
                }
        return Response(response)
"""         except:
            response = {
                "is_active":'False'
            }
            return Response(response) """


@api_view(['GET'])
def available_drivers(request):
    if request.method == 'GET':
        try:
            passenger = request.user.profile
            p_lat = passenger.coordinate_x
            p_lon = passenger.coordinate_y
            print("passenger data succesfully got")
            print("p_lat:", p_lat, " p_lon:", p_lon)
            _passenger = Passenger.objects.get(profile = passenger)
            try:
                if (_passenger.driver != None):
                    message = {
                    'error':'already has a driver'
                    }
                return Response(message, status=status.HTTP_403_FORBIDDEN)
            except:
                pass
        except:
            message = {
                'error':'has not enoght data registered'
            }
            return Response(message, status=status.HTTP_403_FORBIDDEN)

        data = Driver.objects.all()
        print('all passengers successfully gotten')

        drivers = []
        for driver in data:
            try:
                if driver.car.limit>0:
                    print('driver evaluated with space succesfully')
                    lim_d = driver.profile._range
                    d_lat = driver.profile.coordinate_x
                    d_lon = driver.profile.coordinate_y
                    if (d_lat != None and d_lon != None and p_lat != None and p_lon != None and lim_d != None):
                        distance = get_distance(p_lat, p_lon, d_lat, d_lon, lim_d)
                        if(distance != False):
                            drivers.append({
                                "profile_id" : driver.profile.id,
                                "phone": driver.profile.phone,
                                "first_name" : driver.profile.user.first_name,
                                "last_name" : driver.profile.user.last_name,
                                "travel_cost" : driver.car.travel_cost,
                                "limit": driver.car.limit,
                                "distance":distance
                            })
            except:
                pass

        # serializer = DriverSerializer(data=drivers)
        # serializer.is_valid(data=drivers)
        return Response(drivers, status=status.HTTP_200_OK)

class PassengerViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    permissions_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def retrieve(self, request, *args, **kwargs):
        path = request.path.split('/')
        id = path[2]
        print(path)
        try:
            instance = Passenger.objects.get(profile=Profile.objects.get(id=id))
            profile = instance.profile
            distance = get_distance(profile.coordinate_x, profile.coordinate_y, request.user.profile.coordinate_x, request.user.profile.coordinate_y, 100000)
            data = {
                'first_name':profile.user.first_name,
                'last_name':profile.user.last_name,
                'distance':distance
            }
            
            return Response(data)
        except:
            message = {
                "message" : "this passenger does not exist",
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        

class DriverViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permissions_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def retrieve(self, request, *args, **kwargs):
        path = request.path.split('/')
        id = path[2]
        print(path)
        try:
            instance = Driver.objects.get(profile=Profile.objects.get(id=id))
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except:
            message = {
                "message" : "this driver does not exist",
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        
        
""" 
class PassengerListView(ListAPIView):
    '''list all users'''
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
 """
""" class DriverListView(ListAPIView):
    '''list driver's passengers'''

    # def get(request, *args, **kwargs):
    #     driverId = request.user.profile.id

    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination """

""" class DriversPassengers(ListAPIView):
    '''listing the passengers of each driver'''
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
 """

class DriverPassengersViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.DestroyModelMixin):
    serializer_class =  PassengerSerializer
    permissions = []

    def list(self, request, *args, **kwargs):
        driver = request.user.profile.id
        queryset = self.filter_queryset(Passenger.objects.filter(driver=driver))

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        url = request.path.split('/')
        id = url[3]
        driver_id = request.user.profile.id
        instance = Profile.objects.get(id=id)
        passenger = Passenger.objects.get(profile=instance)

        if passenger.driver.id == driver_id:
            passenger.driver.car.limit += 1
            passenger.driver.car.save()
            passenger.driver = None
            passenger.save()
            return Response(status=status.HTTP_200_OK)
        else:
            message = {
                'error':'this passenger is not linked with you'
            }
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    def perform_destroy(self, instance):
        instance.delete()

class PassengerDriver(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):

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

    def destroy(self, request, *args, **kwargs):

        passenger = Passenger.objects.get(profile=request.user.profile)
        passenger.driver.car.limit += 1
        passenger.driver.car.save()
        passenger.driver = None
        passenger.save()
        return Response(status=status.HTTP_200_OK)

class ProfileCompletionViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = EditProfileSerializer
    permission_classes=[]

    def update(self, request, *args, **kwargs):
        id = request.path.split('/')
        id = int(id[2])
        if id != request.user.profile.id:
            return Response('you dont have permission to update this profile', status = status.HTTP_403_FORBIDDEN)
        partial = kwargs.pop('partial', False)
        instance = User.objects.get(profile=Profile.objects.get(id=id))
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        id = request.path.split('/')
        id = id[2] 
        instance = User.objects.get(profile=Profile.objects.get(id=id)) 
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class CarViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permissions = []
    def retrieve(self, request, *args, **kwargs):
        driver_id = request.path.split('/')
        driver_id = driver_id[3]
        print(driver_id)
        instance = Car.objects.get(driver=Driver.objects.get(profile=Profile.objects.get(id=driver_id)))
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

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
