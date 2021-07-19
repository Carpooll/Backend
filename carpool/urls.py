#django
from django.contrib import admin
from django.urls import path, include
#static files
from django.conf import settings
from django.conf.urls.static import static
#Views
from users.views import users
#Rest_framework 
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/signup/', users.signup, name="signup"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)