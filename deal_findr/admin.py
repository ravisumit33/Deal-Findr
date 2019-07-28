from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email']
    for t in UserAdmin.fieldsets:
        if t[0] == 'Personal info':
            t[1]['fields'] = t[1]['fields'] + ('phone',)
            break
  #  fieldsets = UserAdmin.fieldsets + (
   #     (('Personal info'), {'fields': ('phone',)}),
   # )
admin.site.register(CustomUser, CustomUserAdmin)
