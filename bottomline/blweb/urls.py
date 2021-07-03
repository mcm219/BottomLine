from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [path('', views.index, name='landing'),
               path('accounts/profile/', views.profile, name='profile'),
               path('accounts/account_signup/', views.account_signup, name='account_signup'),
               path('accounts/dealer_signup/', views.dealer_signup, name='dealer_signup'),
               path('vehicle_config/', views.vehicle_config, name='vehicle_config'),
               path('vehicle_config_model/', views.vehicle_config_model, name='vehicle_config_model'),
               path('vehicle_config_options/', views.vehicle_config_options, name='vehicle_config_options'),
               ]

