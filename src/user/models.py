from cities_light.models import City, Country, Region
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    address = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.FileField(upload_to="avatars", blank=True, null=True)
    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS = ["username"]


class Individual(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_sole_proprietor = models.BooleanField()
    pass
