from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.contrib.auth.models import User
from users.models import Profile, Car, Driver, Passenger

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'balance')
    list_display_links = ['id', 'user']
    list_editable = ['balance']
    search_fields = ['balance']
    list_filter = ['user__is_active', 'user__is_staff', 'created_at', 'modify_at']

class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural='profiles'

@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile', 'driver']
    list_display_links = ['profile', 'driver']
    search_fields = ['profile']

class PassengerInLine(admin.StackedInline):
    model = Passenger
    can_delete = False
    verbose_name_plural='passengers'

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['id','profile', 'car', 'card_number', 'exp_date']
    list_display_links = ['profile']
    search_fields = ['profile']

class DriverInLine(admin.StackedInline):
    model = Driver
    can_delete = False
    verbose_name_plural='drivers'

class UserAdmin(BaseUserAdmin):
    '''add profile admin to base user admin'''
    inlines = [ProfileInLine]
    list_display = ('username', 'first_name', 'last_name', 'is_active', 'is_staff')
    list_editable = ['is_active', 'is_staff']

admin.site.unregister(User)
admin.site.register(User, UserAdmin)