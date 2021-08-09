#django
from django.contrib import admin
from django.urls import path, include
#static files
from django.conf import settings
from django.conf.urls.static import static
#Views
from users.views.login import UserLoginAPIView as login 
from users.views import users
from notifications.views import notifications
from users.views.users import ProfileCompletionViewSet, DriverPassengersViewSet, PassengerDriver, CarViewSet, PaymentViewSet, DriverViewSet, PassengerViewSet
from notifications.views.notifications import RequestNotificationViewSet, RideNotificationViewSet
from rides.views import createRideViewSet, transaction
#Rest_frameworks
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'profile', ProfileCompletionViewSet, basename='profile')

router.register(r'requests', RequestNotificationViewSet, basename='requests')

router.register(r'driver/passengers', DriverPassengersViewSet, basename='driver_passengers')

router.register(r'passenger/driver', PassengerDriver, basename='pasenger_driver')

router.register(r'driver/car', CarViewSet, basename='car')

router.register(r'driver/payment', PaymentViewSet, basename='payment')

router.register(r'rides', createRideViewSet, basename='rides')

router.register(r'rides/confirmation', RideNotificationViewSet, basename='ride_confirmation')

router.register(r'passengers', PassengerViewSet, basename='passengers')

router.register(r'drivers', DriverViewSet, basename='driver')

urlpatterns = [
    path('admin/', admin.site.urls),
#Sign in and login process
    path('users/login/', login.as_view(), name="login"),  
    path('users/signup/', users.signup, name="signup"),
    path('users/verified/<token>/', users.account_verification, name="verify"),
    path('users/passenger/', users.is_passenger, name="passenger"),
#listing users
#    path('passengers/', users.PassengerListView.as_view(), name="passengers"), 
#    path('drivers/', users.DriverListView.as_view(), name="drivers"),
    path('drivers/available/', users.available_drivers, name="available drivers"),
#notifications
    path('RequestDriver/', notifications.RequestDriver, name="request driver"),
    path('transaction/', transaction, name="transactions"),
    path('',include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)