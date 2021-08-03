from django.db import models
from users.models import Passenger, Driver
# Create your models here.

class Ride (models.Model):
    date = models.DateTimeField(auto_now=True)
    cost = models.IntegerField()
    is_active = models.BooleanField(default=True) 
    driver = models.ForeignKey(Driver, on_delete=models.RESTRICT, null=True, default=None)
    passengers = models.ForeignKey(Passenger, on_delete=models.RESTRICT, null=True, default=None)
        