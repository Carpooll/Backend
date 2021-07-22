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
from users.views.users import ProfileCompletionViewSet
from notifications.views.notifications import RequestNotificationViewSet
#Rest_framework 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'profile', ProfileCompletionViewSet, basename='profile')

router.register(r'requests', RequestNotificationViewSet, basename='requests')

urlpatterns = [
    path('admin/', admin.site.urls),
#Sign in and login process
    path('users/login/', login.as_view(), name="login"),  
    path('users/signup/', users.signup, name="signup"),
    path('users/verified/<token>/', users.account_verification, name="verify"),
    path('users/passenger/', users.is_passenger, name="passenger"),
#lisrring users
    path('passengers/', users.PassengerListView.as_view(), name="passengers"),
    path('drivers/', users.DriverListView.as_view(), name="drivers"),
#notifications
    path('RequestDriver/', notifications.RequestDriver, name="request driver"),

    path('',include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)