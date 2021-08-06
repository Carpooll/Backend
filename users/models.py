from django.db import models
from django.contrib.auth.models import User

class Profile (models.Model):
    ''''user information'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #on username is saved the school id for practice reasons

    phone= models.CharField(max_length=10,default=None, null=True, blank=True)

    created_at = models.DateTimeField(auto_now=True)
    modify_at= models.DateTimeField(auto_now=True)
    balance = models.IntegerField(default=None, null=True, blank=True)
    
    street = models.CharField(max_length=50,default=None, null=True, blank=True)
    suburb = models.CharField(max_length=50,default=None, null=True, blank=True)
    postal_code = models.IntegerField(default=None, null=True, blank=True)
    internal_number = models.IntegerField(blank=True, null=True)
    external_number = models.IntegerField(default=None, null=True, blank=True)
    coordinate_x = models.FloatField(default=None, null=True, blank=True)
    coordinate_y = models.FloatField(default=None, null=True, blank=True)
    _range = models.IntegerField(default=0)

    is_verify = models.BooleanField(default=False)
    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.user.get_full_name()

class Car(models.Model):
    model = models.CharField(max_length=100, blank=True, null=True)
    Colors = (
        ('1', 'Red'),
        ('2', 'Black'),
        ('3', 'Black'),
        ('4', 'Yellow'),
        ('5', 'Orange'),
        ('6', 'Blue'),
    )
    color = models.CharField(max_length=1, choices=Colors,  blank=True, null=True)
    plates = models.CharField(max_length=10, blank=True, null=True)
    insurance = models.CharField(max_length=100,  blank=True, null=True)
    limit = models.IntegerField(blank=True, null=True)
    travel_cost = models.IntegerField(blank=True, null=True)


class Driver (models.Model):

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='DriverProfile')
    card_owner= models.CharField(max_length=100, default=None, null=True, blank=True)
    car = models.OneToOneField(Car, on_delete=models.CASCADE, null=True, blank=True)
    ''''payment information'''
    card_number = models.CharField(max_length=16, null=True, blank=True)
    exp_date = models.CharField(max_length=5, default=None, null=True, blank=True)
    ccv = models.IntegerField(null=True, blank=True)

class Passenger(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='PassengerProfile')

    driver = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='driver')
