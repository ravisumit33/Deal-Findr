from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from . import models

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = models.CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = models.CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone',)

class CustomerForm(forms.Form):
    WEBSITE_CHOICES = (
        ('Choose Website', 'Choose Website'),
        ('Amazon', 'Amazon'),
        ('Flipkart', 'Flipkart'),
        ('Snapdeal', 'Snapdeal'),
        ('Myntra', 'Myntra'),
    )

    website = forms.ChoiceField(
        choices=WEBSITE_CHOICES,
        initial={'Choose Website' : 'Choose Website'},
        widget=forms.Select(
            attrs={
                'class' : 'selection-2'
                }
            )
        )

    budget = forms.IntegerField(
            widget=forms.NumberInput(
                attrs={
                    'class' : 'input100',
                    'placeholder' : 'Enter your budget'
                    }
                )
            )

    productURL =  forms.URLField(
            widget=forms.URLInput(
                attrs={
                    'class' : 'input100',
                    'placeholder' : 'Enter product URL'
                    }
                )
            )
    
