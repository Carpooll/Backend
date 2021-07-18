from django.db import models
from django.contrib.auth.models import User

class Payment(models.Model):
    ''''payment information'''
    card_number = models.CharField(max_length=16)
    exp_date = models.CharField(max_length=5)
    ccv = models.IntegerField()

class Adress(models.Model):
    street = models.CharField(max_length=50)
    suburb = models.CharField(max_length=50)
    postal_code = models.IntegerField()
    internal_number = models.IntegerField(blank=True, null=True)
    external_number = models.IntegerField()
    coordinate_x = models.IntegerField()


class Profile (models.Model):
    ''''user information'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school_id = models.IntegerField(unique=True)

    first_name= models.CharField(max_length=100)
    last_name= models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now=True)
    modify_at= models.DateTimeField(auto_now=True)
    balance = models.IntegerField()
    adress = models.OneToOneField(Adress,null = True, on_delete=models.CASCADE)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    is_verfy = models.BooleanField(default=False)
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

    car = models.OneToOneField(Car, on_delete=models.CASCADE)


class Passenger(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    driver = models.OneToOneField(Driver, on_delete=models.CASCADE)
