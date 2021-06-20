from django import forms
from enum import Enum
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AccountType(Enum):
    SHOPPER = 1
    DEALER = 2
    ADMIN = 3


# The superclass for the specific user signup forms (shopper and dealer)
class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=100)
    phone = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2')

