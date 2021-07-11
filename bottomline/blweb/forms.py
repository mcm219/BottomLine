from django import forms
from enum import Enum
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from blweb.models import VehicleMake, VehicleModel, VehicleOption, VehicleColor


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

    name = forms.ModelChoiceField(queryset=VehicleMake.objects.all().order_by('name'), label='Vehicle Make')

    class Meta:
        model = VehicleMake
        fields = ['name']


class VehicleModelForm(forms.ModelForm):

    class Meta:
        model = VehicleModel
        fields = ['name']

    def __init__(self, *args, **kwargs):

        self.chosen_make = kwargs.pop('chosen_make', None)
        super(VehicleModelForm, self).__init__(*args, **kwargs)
        if self.chosen_make is not None:
            self.fields['name'].queryset = VehicleModel.objects.filter(make__name=self.chosen_make).order_by('name')
        else:
            self.fields['name'].queryset = VehicleModel.objects.distinct().order_by('name')

    name = forms.ModelChoiceField(queryset=VehicleModel.objects.distinct().order_by('name'), label='Vehicle Model')

    def save(self, **kwargs):
        self.full_clean()
        return super(VehicleModelForm, self).save(**kwargs)

    def clean_name(self):
        return self.cleaned_data['name']

    def clean(self):
        cleaned_data = super(VehicleModelForm, self).clean()

        # check to see if this instance has an associated make
        if self.chosen_make is None:
            raise ValidationError(
                "No VehicleMake associated with this instance."
            )
        return cleaned_data


class VehicleOptionsForm(forms.ModelForm):
    class Meta:
        model = VehicleOption
        #fields = ['name']
        fields = []

    def __init__(self, *args, **kwargs):

        self.chosen_model = kwargs.pop('chosen_model', None)
        super(VehicleOptionsForm, self).__init__(*args, **kwargs)
        if self.chosen_model is not None:
            self.fields['options'].queryset = VehicleOption.objects.filter(model=self.chosen_model).\
                exclude(vehiclecolor__isnull=False).order_by('name')
        else:
            self.fields['options'].queryset = VehicleOption.objects.distinct().\
                exclude(vehiclecolor__isnull=False).order_by('name')

    options = forms.ModelMultipleChoiceField(queryset=VehicleOption.objects.distinct().order_by('name'),
                                             widget=forms.CheckboxSelectMultiple,
                                             required=False)

    def clean(self):
        cleaned_data = super(VehicleOptionsForm, self).clean()

        # check to make sure all the options selected actually belong to the appropriate vehicle model
        for option in cleaned_data.get('options').all():
            if option.model.pk != self.chosen_model:
                raise ValidationError(
                    "Option does not exist for the chosen vehicle make/model."
                )
        return cleaned_data


# provide the form choices for vehicle colors as well
class VehicleColorOptionsForm(forms.ModelForm):
    class Meta:
        model = VehicleColor
        fields = []

    def __init__(self, *args, **kwargs):

        self.chosen_model = kwargs.pop('chosen_model', None)
        super(VehicleColorOptionsForm, self).__init__(*args, **kwargs)
        if self.chosen_model is not None:
            self.fields['colors'].queryset = VehicleColor.objects.filter(model=self.chosen_model).order_by('name')
        else:
            self.fields['colors'].queryset = VehicleColor.objects.filter(model=self.chosen_model).order_by('name')

        # now set the default color
        if VehicleColor.objects.filter(model=self.chosen_model).count() > 0:
            self.fields['colors'].initial = VehicleColor.objects.filter(model=self.chosen_model).order_by('name')[0].pk

    colors = forms.ModelChoiceField(queryset=VehicleColor.objects.distinct().order_by('name'),
                                    widget=forms.RadioSelect,
                                    required=False)
