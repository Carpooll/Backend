from django.db import models
from users.models import Profile, Driver, Passenger
from django.contrib.auth.models import User
# Create your models here.
class Notification(models.Model):
    date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=150,null=True, blank=True)
    sendee = models.ForeignKey(User, on_delete=models.CASCADE)

class Request(models.Model):
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE)
    sender = models.OneToOneField(User, on_delete=models.CASCADE)

