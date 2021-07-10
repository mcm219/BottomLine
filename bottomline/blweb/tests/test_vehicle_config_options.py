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

    # test that the page is found
    def test_options_page_exists(self):
        # create a test VehicleConfig from the make above
        veh_config = VehicleConfig.objects.create(make=self.make,
                                                  model=self.model)
        veh_config.save()

        # set the required session variable
        session = self.client.session
        session['vehicle_config'] = veh_config.pk
        session.save()

        response = self.client.get('/vehicle_config_options/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='vehicle_config_options.html')

    def test_something_else(self):
        pass
