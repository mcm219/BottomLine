from django.http import SimpleCookie
from django.test import TestCase
from django.test import Client

from blweb.forms import VehicleOptionsForm, VehicleColorOptionsForm
from blweb.models import VehicleMake, VehicleConfig, VehicleColor
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

    def test_options_form(self):
        # create a test VehicleConfig from the make above
        veh_config = VehicleConfig.objects.create(make=self.make,
                                                  model=self.model,
                                                  color=self.paint_color)
        veh_config.save()

        # set the required session variable
        session = self.client.session
        session['vehicle_config'] = veh_config.pk
        session.save()

        form = VehicleOptionsForm(prefix='options',
                                  chosen_model=veh_config.model.pk,
                                  data={'options-options': [self.option1.pk, self.option2.pk]})

        self.assertTrue(form.is_valid())

    def test_colors_form(self):
        # create a test VehicleConfig from the make above
        veh_config = VehicleConfig.objects.create(make=self.make,
                                                  model=self.model,
                                                  color=self.paint_color)
        veh_config.save()

        # set the required session variable
        session = self.client.session
        session['vehicle_config'] = veh_config.pk
        session.save()

        form = VehicleColorOptionsForm(prefix='colors',
                                       chosen_model=veh_config.model.pk,
                                       data={'colors': self.paint_color.pk})

        self.assertTrue(form.is_valid())

    # test the options form field names
    def test_vehicle_options_form_fields(self):
        form = VehicleOptionsForm()
        self.assertIn("options", form.fields)

    # test the colors form field names
    def test_vehicle_color_options_form_fields(self):
        form = VehicleColorOptionsForm()
        self.assertIn("colors", form.fields)


