from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from . import models

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = models.CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = models.CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone',)

class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Deal
        fields = ('website', 'budget', 'productURL',)
