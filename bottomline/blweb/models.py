from django.db import models

class VehicleMake(models.Model):
    """A brand of vehicle manufacture"""
    name = models.CharField(max_length=50,
                            help_text="The name of the vehicle make")
    website = models.URLField(help_text="The official website for this vehicle make")

class VehicleModel(models.Model):
    """A model of vehicle for a particular make"""
    name = models.CharField(max_length=100,
                            help_text="The name of the vehicle model")
    year = models.IntegerField(help_text="The model year for this model")



