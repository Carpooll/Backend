from django.db import models
from users.models import Profile, Driver, Passenger
from django.contrib.auth.models import User
# Create your models here.
class Notification(models.Model):
    date = models.DateTimeField(auto_now=True, null=True, blank=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    text = models.CharField(max_length=150,null=True, blank=True)
    sendee = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='the_sender', null=True, blank=True)
class Request(models.Model):
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE)
    status_options = {
        ('1', 'pending'),
        ('2', 'accepted'),
        ('3', 'denied')
    }
    status = models.CharField(choices=status_options, max_length=1, default=1)
