from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractUser):
    phone = PhoneNumberField()


class Deals(models.Model):
    customer = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    website = models.CharField(max_length=50)

