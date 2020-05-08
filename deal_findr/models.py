from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractUser):
    phone = PhoneNumberField()


class Deal(models.Model):
    WEBSITE_CHOICES = (
        ('Choose Website', 'Choose Website'),
        ('Amazon', 'Amazon'),
        ('Flipkart', 'Flipkart'),
        ('Snapdeal', 'Snapdeal'),
        ('Myntra', 'Myntra'),
    )
    customer = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    website = models.CharField(
        max_length=14,
        choices = WEBSITE_CHOICES,
        default = 'Choose Website'
    )
    budget = models.DecimalField(max_digits=10, decimal_places=3)
    productURL = models.URLField(max_length=2000)
    productName = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
