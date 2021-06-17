from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [path('', views.index, name='landing'),
               path('accounts/profile/', views.profile, name='profile'),
               path('accounts/account_signup/', views.account_signup, name='account_signup'),
               path('accounts/dealer_signup/', views.dealer_signup, name='dealer_signup'),
               ]

