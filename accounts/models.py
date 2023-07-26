from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from base import constants


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class InActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=False)


class CustomUser(AbstractUser):
    """Custom User Model that takes extra fields for easier authentication"""
    HOUSE_OWNER = constants.HOUSE_OWNER
    TENANT = constants.TENANT
    
    SIGN_UP_CHOICES = (
        ('House Owner', HOUSE_OWNER),
        ('Tenants', TENANT),
    )

    first_name = models.CharField(max_length=30, null=False, blank=False)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    username = models.CharField(max_length=19, unique=True, blank=True)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField(unique=True)
    signuptype = models.CharField(max_length=200, choices=SIGN_UP_CHOICES, blank=False, null=False, default= "H.O")
    phone_number = PhoneNumberField(unique=True, null=True)
    profile_picture = models.ImageField(upload_to="images/user_profile_picture", default="avatar.svg")
    address = models.CharField(max_length=300, blank=True, null=True)
    # twitter_link= models.URLField()
    # facebook_link= models.URLField()
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = UserManager()
    active_objects = ActiveManager()
    inactive_objects = InActiveManager()

    def __str__(self):
        return self.username
    
    @property
    def image_URL(self):
        try:
            url = self.profile_picture.url
        except AttributeError:
            url = ''
        return url


class HouseOwner(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.user.username

class Tenant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.user.username

