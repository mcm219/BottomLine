from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from blweb.forms import AccountType


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.IntegerField(help_text="The type of account (dealer or shopper)",
                                       default=AccountType.SHOPPER.value)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


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

