from django.http import SimpleCookie
from django.template.loader import render_to_string
from django.test import TestCase
from django.test import Client

from blweb.forms import VehicleOptionsForm, VehicleColorOptionsForm
from blweb.models import VehicleMake, VehicleConfig, VehicleColor
from blweb.models import VehicleModel
from blweb.models import VehicleOption

# Test class for unit tests on the vehicle config options
from blweb.views import add_option_price_context_dict, add_color_option_price_context_dict


class TestVehicleConfigHistory(TestCase):
    # set up the environment
    def setUp(self):
        self.client = Client()
        # first create a test make
        self.make = VehicleMake.objects.create(
            name='Ferrari',
            website='www.ferrari.com',
        )
        # now a test model
        self.model = VehicleModel.objects.create(
            name='Roma',
            year=2021,
            make=self.make
        )

        self.option1 = VehicleOption.objects.create(name='Carbon Buckets',
                                                    description='Race-inspired carbon fiber bucket seats',
                                                    price=5000,
                                                    model=self.model)

        self.option2 = VehicleOption.objects.create(name='Shadowline Trim Package',
                                                    description='Enhance the look of your Ferrari with blacked out trim',
                                                    price=4350,
                                                    model=self.model)

        self.paint_color = VehicleColor.objects.create(name='Rosso Corsa',
                                                       description='The original color of Ferrari Racing',
                                                       price=1000,
                                                       model=self.model)

        self.ford = VehicleMake.objects.create(name='Ford',
                                               website='www.ford.com')
        self.mustang = VehicleModel.objects.create(name='Mustang',
                                                   year=2021,
                                                   make=self.ford)
        self.pp1 = VehicleOption.objects.create(name='Performance Pack 1',
                                                description='Mustang Performance Pack 1',
                                                price=3000,
                                                model=self.mustang)
