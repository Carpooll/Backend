from django.db import models
from users.models import Passenger, Driver, Profile
# Create your models here.

class Ride (models.Model):
    date = models.DateTimeField(auto_now=True)
    cost = models.IntegerField()
    is_active = models.BooleanField(default=True) 
    driver = models.ForeignKey(Profile, on_delete=models.RESTRICT)

    passenger1 = models.IntegerField(default=None, null=True, blank=True)
    passenger2 = models.IntegerField(default=None, null=True, blank=True)
    passenger3 = models.IntegerField(default=None, null=True, blank=True)
    passenger4 = models.IntegerField(default=None, null=True, blank=True)
    passenger5 = models.IntegerField(default=None, null=True, blank=True)
    passenger6 = models.IntegerField(default=None, null=True, blank=True)
