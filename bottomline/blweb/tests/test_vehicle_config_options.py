from django.http import SimpleCookie
from django.test import TestCase
from django.test import Client

from blweb.forms import VehicleMakeForm, VehicleModelForm
from blweb.models import VehicleMake, VehicleConfig
from blweb.models import VehicleModel
from blweb.models import VehicleOption


# Test class for unit tests on the vehicle config options
class TestVehicleConfigOptions(TestCase):
    # set up the environment
    def setUp(self):
        self.client = Client()
        self.veh_make = "BMW"
        self.veh_model = "M3"

    # test that the page is found
    def test_options_page_exists(self):
        pass


    def test_something_else(self):
        pass
