from django.contrib.auth.models import User
from django.http import SimpleCookie
from django.template.loader import render_to_string
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from blweb.forms import VehicleOptionsForm, VehicleColorOptionsForm
from blweb.models import VehicleMake, VehicleConfig, VehicleColor, AccountType
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

        # create some test options
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

        # create a user
        self.test_shopper = User.objects.create_user(username='testshopper', password='test@#628password')
        self.test_shopper.profile.account_type = AccountType.SHOPPER.value
        self.test_shopper.save()

    # check to see if the page is present
    def test_config_history_page_present(self):
        # user needs to be logged in to see the page
        self.client.force_login(self.test_shopper)

        response = self.client.get('/view_configs/')
        self.assertEqual(response.status_code, 200)

    # check that the proper view was used (dealer)
    def test_config_history_view_name(self):
        # user needs to be logged in to see the page
        self.client.force_login(self.test_shopper)

        response = self.client.get(reverse('view_configs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='view_configs.html')

    # check to see that the Profile link is present on the profile page
    def test_config_history_link(self):
        # user needs to be logged in to see the page
        self.client.force_login(self.test_shopper)

        response = self.client.get(reverse('profile'))
        self.assertContains(response, text="View my vehicle configurations")

    # check that the config history page does not load when logged out
    def test_config_history_logged_out(self):
        # user needs to be logged in to see the page
        self.client.logout()

        response = self.client.get(reverse('view_configs'))
        self.assertEqual(response.status_code, 302)

    # check to see if the page has the test config
    def test_config_history_config_present(self):
        # user needs to be logged in to see the page
        self.client.force_login(self.test_shopper)

        # create a test VehicleConfig from the make above
        veh_config = VehicleConfig.objects.create(make=self.make,
                                                  model=self.model,
                                                  color=self.paint_color,
                                                  user=self.test_shopper,
                                                  config_name='My Test Config!')
        veh_config.save()

        response = self.client.get('/view_configs/')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, text='My Test Config')

    # check that the GET parameter passing works
    def test_config_history_get_params(self):
        # user needs to be logged in to see the page
        self.client.force_login(self.test_shopper)

        # create a test VehicleConfig from the make above
        veh_config = VehicleConfig.objects.create(make=self.make,
                                                  model=self.model,
                                                  color=self.paint_color,
                                                  user=self.test_shopper,
                                                  config_name='My Test Config!')
        veh_config.save()

        url = f'/vehicle_config_complete/?config_id={veh_config.pk}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, text='Ferrari')

    # check that the config history page contains the proper link to the details for the config shown
    def test_config_history_link_to_details(self):
        # user needs to be logged in to see the page
        self.client.force_login(self.test_shopper)

        # create a test VehicleConfig from the make above
        veh_config = VehicleConfig.objects.create(make=self.make,
                                                  model=self.model,
                                                  color=self.paint_color,
                                                  user=self.test_shopper,
                                                  config_name='My Test Config!')
        veh_config.save()

        url = f'/vehicle_config_complete/?config_id={veh_config.pk}'
        response = self.client.get('/view_configs/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text=url)

