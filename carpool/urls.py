#django
from django.contrib import admin
from django.urls import path, include
#static files
from django.conf import settings
from django.conf.urls.static import static
#Views
from users.views import users
from users.views.users import ProfileCompletionViewSet
#Rest_framework 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'profile', ProfileCompletionViewSet, basename='profile')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/signup/', users.signup, name="signup"),
    path('users/verified/<token>/', users.account_verification, name="verify"),
    path('users/args_demo/<si>/', users.args_demo, name="demo"),
    path('',include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)