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
    color = models.CharField(max_length=1, choices=Colors)
    plates = models.IntegerField()
    insurance = models.CharField(max_length=100)
    limit = models.IntegerField()
    travel_cost = models.IntegerField()


class Driver (models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    card_owner= models.CharField(max_length=100, default=None)
    car = models.OneToOneField(Car, on_delete=models.CASCADE)
    ''''payment information'''
    card_number = models.CharField(max_length=16, )
    exp_date = models.CharField(max_length=5, default=None)
    ccv = models.IntegerField()

class Passenger(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    driver = models.OneToManyField(Driver, on_delete=models.CASCADE)
