from django.db import models

class VehicleMake(models.Model):
    """A brand of vehicle manufacture"""
    name = models.CharField(max_length=50,
                            help_text="The name of the vehicle make")
    website = models.URLField(help_text="The official website for this vehicle make")

