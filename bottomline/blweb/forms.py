from django import forms
from enum import Enum
from django.contrib.auth.password_validation import validate_password


class AccountType(Enum):
    SHOPPER = 1
    DEALER = 2


# The superclass for the specific user signup forms (shopper and dealer)
class SignupForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    email = forms.EmailField()
    phone = forms.CharField(required=False)
    account_type = None


# add the fields specific to the customer
class ShopperSignupForm(SignupForm):
    account_type = AccountType.SHOPPER


# add fields specific to the car dealer
class DealerSignupForm(SignupForm):
    account_type = AccountType.DEALER
