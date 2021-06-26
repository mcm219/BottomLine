from django import forms
from enum import Enum
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from blweb.models import VehicleMake, VehicleModel


# The superclass for the specific user signup forms (shopper and dealer)
class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=100)
    phone = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2')


class VehicleConfigForm(forms.Form):

    # get a list of all makes in the make model currently
    #makes = [name['name'] for name in VehicleMake.objects.all()]
    #make = forms.CharField(choices=makes)
    #model = forms.CharField(choices=)
    pass




