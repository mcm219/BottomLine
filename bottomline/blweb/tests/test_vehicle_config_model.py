from django.contrib.auth.models import User
from django.test import TestCase
from blweb.models import VehicleMake, VehicleConfig
from blweb.models import VehicleModel
from blweb.models import VehicleOption


# Test class for unit tests on the vehicle config data model class
class TestVehicleConfigModel(TestCase):
    # CRUD tests
    # set up the environment
    def setUp(self):
        self.ford = VehicleMake.objects.create(name="Ford", website="www.ford.com")
        self.mustang = VehicleModel.objects.create(name='Mustang', year=2021, make=self.ford)

        option = VehicleOption.objects.create(name="Performance Pack 1",
                                              description="Brakes, shocks, and spoiler added",
                                              price=2000,
                                              model=self.mustang)
        option.save()
        self.options = []
        self.options.append(option)
        self.user = User.objects.create_user(username='testuser', password='test@#628password')

        self.config = VehicleConfig(config_name="my mustang",
                                    make=self.ford,
                                    model=self.mustang,
                                    user=self.user)
        self.config.save()
        self.config.options.add(self.options[0])

    # test that we can create a new vehicle option
    def test_insert_vehicle_config(self):
        self.assertIsInstance(self.config, VehicleConfig)

    # test that we can select/read a vehicle option from the data model
    def test_select_vehicle_config(self):
        self.assertEqual(str(self.config), "my mustang")

    # test that the config is linked to the make
    def test_vehicle_make_from_config(self):
        self.assertEqual(self.config.make, self.ford)

    # test that the config is linked to the model
    def test_vehicle_model_from_config(self):
        self.assertEqual(self.config.model, self.mustang)

    # test that the config is linked to the options
    def test_vehicle_options_from_config(self):
        self.assertEqual(self.config.options.get(id=self.options[0].pk), self.options[0])

    def test_vehicle_user_from_config(self):
        self.assertEqual(self.config.user, self.user)

    # test that we can delete a vehicle config model
    def test_delete_vehicle_option(self):
        # first delete the object
        self.config.delete()

        # now make sure we can't get any more objects
        self.assertEqual(VehicleConfig.objects.count(), 0)
