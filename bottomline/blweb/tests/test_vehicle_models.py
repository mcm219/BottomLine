from django.test import TestCase
from blweb.models import VehicleMake
from blweb.models import VehicleModel
from blweb.models import VehicleOption


# Test class for unit tests on the vehicle data model classes
class TestVehicleMake(TestCase):

    # CRUD tests
    # set up the environment
    def setUp(self):
        self.ford = VehicleMake.objects.create(name="Ford", website="www.ford.com")

    # Vehicle Make CRUD tests
    # test that we can create a new vehicle make
    def test_create_vehicle_make(self):
        self.assertIsInstance(self.ford, VehicleMake)

    # test that we can select/read a vehicle make from the model
    def test_read_vehicle_make_name(self):
        self.assertEqual(str(self.ford), "Ford")

    # test that we can delete a vehicle make
    def test_delete_vehicle_make(self):
        # first delete the object
        self.ford.delete()

        # now make sure we can't get any more objects
        self.assertEqual(VehicleMake.objects.count(), 0)

    # cleanup the test environment
    def tearDown(self):
        pass


# VehicleModel CRUD tests
class TestVehicleModel(TestCase):
    # set up the environment
    def setUp(self):
        self.ford = VehicleMake.objects.create(name="Ford", website="www.ford.com")
        self.mustang = VehicleModel.objects.create(name="Mustang", year=2021, make=self.ford)

    # test that we can create a new vehicle model
    def test_insert_vehicle_model(self):
        self.assertIsInstance(self.mustang, VehicleModel)

    # test that we can select/read a vehicle model from the model
    def test_select_vehicle_model(self):
        self.assertEqual(str(self.mustang), "Mustang")

    # test that the model is linked to the make
    def test_vehicle_make_from_model(self):
        self.assertEqual(self.mustang.make, self.ford)

    # test that we can delete a vehicle model
    def test_delete_vehicle_model(self):
        # first delete the object
        self.mustang.delete()

        # now make sure we can't get any more objects
        self.assertEqual(VehicleModel.objects.count(), 0)

    # cleanup the test environment
    def tearDown(self):
        pass


# VehicleModel CRUD tests
class TestVehicleOptions(TestCase):
    # set up the environment
    def setUp(self):
        self.ford = VehicleMake.objects.create(name="Ford", website="www.ford.com")
        self.mustang = VehicleModel.objects.create(name="Mustang", year=2021, make=self.ford)
        self.pp1 = VehicleOption.objects.create(name="Performance Pack 1",
                                                description="Brakes, shocks, and spoiler added",
                                                price=2000,
                                                model=self.mustang)

    # test that we can create a new vehicle option
    def test_insert_vehicle_option(self):
        self.assertIsInstance(self.pp1, VehicleOption)

    # test that we can select/read a vehicle option from the data model
    def test_select_vehicle_option(self):
        self.assertEqual(str(self.pp1), "Performance Pack 1")

    # test that the option is linked to the model
    def test_vehicle_model_from_option(self):
        self.assertEqual(self.pp1.model, self.mustang)

    # test that we can delete a vehicle model
    def test_delete_vehicle_option(self):
        # first delete the object
        self.pp1.delete()

        # now make sure we can't get any more objects
        self.assertEqual(VehicleOption.objects.count(), 0)

    # cleanup the test environment
    def tearDown(self):
        pass
