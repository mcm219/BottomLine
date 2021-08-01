from enum import Enum

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from localflavor.us.models import USZipCodeField, USStateField


class AccountType(Enum):
    SHOPPER = 1
    DEALER = 2
    ADMIN = 3


class VehicleMake(models.Model):
    """A brand of vehicle manufacture"""
    name = models.CharField(max_length=50,
                            help_text="The name of the vehicle make")
    website = models.URLField(help_text="The official website for this vehicle make")

    def __str__(self):
        return self.name


class VehicleModel(models.Model):
    """A model of vehicle for a particular make"""
    name = models.CharField(max_length=100,
                            help_text="The name of the vehicle model")
    year = models.IntegerField(help_text="The model year for this model")
    make = models.ForeignKey(VehicleMake,
                             on_delete=models.CASCADE,
                             default=None,
                             help_text="The vehicle make that this model is associated with")
    price = models.IntegerField(default=0,
                                help_text="The base MSRP for the model, not including options")

    def __str__(self):
        return self.name


class VehicleOption(models.Model):
    name = models.CharField(max_length=200,
                            help_text="The name of the vehicle option")
    description = models.TextField(help_text="A description of the option package and what features it includes")
    price = models.IntegerField(help_text="The price for this option")
    model = models.ForeignKey(VehicleModel,
                              on_delete=models.CASCADE,
                              default=None,
                              help_text="The vehicle model associated with this option package")

    def __str__(self):
        return self.name


# extend the VehicleOption class to specifically call out colors, which are like options
# but may have some unique attributes eventually (e.g. flat, metallic, matte)
class VehicleColor(VehicleOption):
    pass


class Address(models.Model):
    street = models.CharField(max_length=200,
                              help_text="The street address, e.g. 123 Main St.")
    city = models.CharField(max_length=100,
                            help_text="The city for this address, e.g. Farmville")
    zip_code = USZipCodeField(help_text="The address Zip Code, e.g. 90210")
    state = USStateField(help_text="The address state, e.g. PA")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.IntegerField(help_text="The type of account (dealer or shopper)",
                                       default=AccountType.SHOPPER.value)
    address = models.ForeignKey(Address,
                                on_delete=models.CASCADE,
                                default=None,
                                null=True,
                                blank=True,
                                help_text="The US mailing address associated with this account (optional)")

    # Note: Only applies for AccountType.DEALER accounts
    dealer_make = models.ForeignKey(VehicleMake,
                                    on_delete=models.CASCADE,
                                    default=None,
                                    null=True,
                                    blank=True,
                                    help_text="The vehicle make associated with this dealer")


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


# VehicleConfig class. Models the build a user would put together on the site.
# captures the make, model, color and options.
class VehicleConfig(models.Model):
    config_name = models.CharField(max_length=200,
                                   help_text="The name of this vehicle configuration",
                                   default=None,
                                   null=True,
                                   blank=True)
    make = models.ForeignKey(VehicleMake,
                             on_delete=models.CASCADE,
                             default=None,
                             help_text="The vehicle make associated with this build")
    model = models.ForeignKey(VehicleModel,
                              on_delete=models.CASCADE,
                              default=None,
                              null=True,
                              blank=True,
                              help_text="The vehicle model associated with this option package")
    options = models.ManyToManyField(VehicleOption,
                                     blank=True,
                                     help_text="List of options selected in this config")

    color = models.ForeignKey(VehicleColor,
                              on_delete=models.CASCADE,
                              default=None,
                              null=True,
                              blank=True,
                              related_name='color',
                              help_text="The chosen color for this config")

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True,
                             default=None,
                             help_text="The user associated with this vehicle configuration")

    def __str__(self):
        if self.config_name is None:
            return "New " + str(self.make)
        else:
            return self.config_name
