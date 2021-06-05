from django.db import models


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

