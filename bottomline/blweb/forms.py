from django import forms
from enum import Enum
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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

    def __init__(self, chosen_make=None, *args, **kwargs):
        super(VehicleConfigForm, self).__init__(*args, **kwargs)
        self.chosen_make = chosen_make
        #if self.chosen_make is not None:
        #    model = forms.ModelChoiceField(queryset=VehicleModel.objects.filter(make=self.chosen_make))
        #else:
        #    model = forms.ModelChoiceField(queryset=None, widget=forms.HiddenInput())

    # get a list of all makes in the make model currently
    make = forms.ModelChoiceField(queryset=VehicleMake.objects.all().order_by('name'),
                                  widget=forms.Select(attrs={'onchange': 'makes.submit();'}))


class VehicleMakeForm(forms.ModelForm):

    name = forms.ModelChoiceField(queryset=VehicleMake.objects.all().order_by('name'))

    class Meta:
        model = VehicleMake
        fields = ['name']


class VehicleModelForm(forms.ModelForm):
    def __init__(self, chosen_make=None, *args, **kwargs):
        super(VehicleModelForm, self).__init__(*args, **kwargs)
        self.chosen_make = chosen_make

    name = forms.ModelChoiceField(queryset=VehicleModel.objects.all().order_by('name'))

    class Meta:
        model = VehicleModel
        fields = ['name']

    def clean(self):
        cleaned_data = super().clean()

        # check to see if this instance has an associated make
        if self.chosen_make is None:
            raise ValidationError(
                "No VehicleMake associate with this instance."
            )
        return cleaned_data

