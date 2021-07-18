from django.contrib import admin
from django.urls import path

#Static files 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
]
