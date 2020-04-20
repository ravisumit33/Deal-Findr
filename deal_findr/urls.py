from django.urls import path, include
from . import views

app_name = 'deal_findr'
urlpatterns = [
    path('', views.HomeView, name='home'),
    path('form/', views.FormView, name='form'),
    path('accounts/signup/', views.SignUp.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
]
