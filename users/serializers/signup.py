'''Creating serializer to register a new user'''
#django
from django.contrib.auth import password_validation
from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
#rest_framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
#models
from django.contrib.auth.models import User
from users.models import Profile
#utilities
import jwt
from datetime import timedelta


class UserSignupSerializer(serializers.Serializer):
    """"""

    #School id is saved on username as a unique field
    username = serializers.CharField(
        min_length=10,
        max_length=10,
        allow_blank=False,
    validators=[UniqueValidator(queryset=User.objects.all())])

    email = serializers.EmailField(
        max_length=150,
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all())])

    password = serializers.CharField(
        min_length=8, 
        max_length=128, 
        allow_blank=False)

    password_confirmation = serializers.CharField(
        min_length=8, 
        max_length=128, 
        allow_blank=False)

    
    def validate(self,data):

        passwd = data['password']
        passwd_conf = data['password_confirmation']

        if passwd != passwd_conf:
            raise serializers.ValidationError({'Error':'Passwords do not match'})
        password_validation.validate_password(passwd)

        return data
    
    def create(self,data):
        data.pop('password_confirmation')
        user = User.objects.create_user(
            username=data['username'], 
            password=data['password'],
            email=data['email']
        )
        profile = Profile(user=user)
        profile.save()
        token, create = Token.objects.get_or_create(user=user)

        return user.id, token.key

    def send_confirmation_email(self, user):
        """"send confirmation email """
        verification_token = self.gen_verification_token(user)
        subject = f'Welcome @{user.username}! verify your account'
        from_email ='Application <noreply@app.com'
        content =  render_to_string(
            'emails/account_verification.html',
            {'token': verification_token, 'user': user}
        )
        msg = EmailMultiAlternatives(
            subject, content,from_email, [user.email],
        )
        msg.attach_alternative(content, 'text/html')
        msg.send()
        
    def gen_verification_token(self, user):
        expire_date = timezone.now() + timedelta(days=3)
        payload = {
            'user':user.username,
            'exp':int(expire_date.timestamp()),
            'type':'email_confirmation'
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token