from django.http import SimpleCookie
from django.test import TestCase
from django.test import Client

from blweb.forms import VehicleMakeForm, VehicleModelForm
from blweb.models import VehicleMake
from blweb.models import VehicleModel
from blweb.models import VehicleOption


# Test class for unit tests on the vehicle data model classes
class TestVehicleConfig(TestCase):

    # CRUD tests
    # set up the environment
    def setUp(self):
        self.client = Client()
        self.veh_make = "BMW"
        self.veh_model = "M3"

    # test the vehicle config make page exists
    def test_vehicle_make_page_exists(self):
        response = self.client.get('/vehicle_config/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='vehicle_config_make.html')

    # test the vehicle config model page exists (with cookie)
    def test_vehicle_model_page_exists(self):
        # set the cookie needed (as if we came from the make page)
        self.client.cookies = SimpleCookie({'VehicleMake': 'BMW'})
        response = self.client.get('/vehicle_config_model/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='vehicle_config_model.html')

    # test that without the cookie, the user gets redirected back to the main config page
    def test_vehicle_model_no_cookie_redirect(self):
        response = self.client.get('/vehicle_config_model/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='vehicle_config_make.html')

    # test a form post from the make page
    # def test_vehicle_make_post(self):
    #     response = self.client.post('/vehicle_config/', {'make-name': '51'}, follow=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, template_name='vehicle_config_model.html')
    #
    # # test good data in the VehicleMakeForm
    def test_vehicle_make_form(self):

        make = VehicleMake.objects.create(
            name='Ferrari',
            website='www.ferrari.com',
        )

        form = VehicleMakeForm({'name': make.pk})

        self.assertTrue(form.is_valid())

    # test bad data in the VehicleMakeForm
    def test_vehicle_make_form_bad(self):
        make = VehicleMake.objects.create(
            name='Ferrari',
            website='www.ferrari.com',
        )

        form = VehicleMakeForm({'name': 'problems'})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors.keys())
        self.assertIn('Select a valid choice. That choice is not one of the available choices.', form.errors['name'])

    # test  VehicleMakeForm name field
    def test_vehicle_make_form_fields(self):
        form = VehicleMakeForm()
        self.assertIn("name", form.fields)

    # test  VehicleModelForm name field
    def test_vehicle_model_form_fields(self):
        form = VehicleModelForm()
        self.assertIn("name", form.fields)