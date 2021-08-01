from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client

# Test class for unit tests on the dealer location
from django.urls import reverse

from blweb.models import AccountType, Address, VehicleMake


class TestDealerAffiliation(TestCase):

    # any needed setup for the tests. this function will be run before every test case
    def setUp(self):
        self.test_shopper = User.objects.create_user(username='testshopper', password='test@#628password')
        self.test_shopper.profile.account_type = AccountType.SHOPPER.value
        self.test_shopper.save()

        self.test_dealer = User.objects.create_user(username='testdealer', password='test@#628password')
        self.test_dealer.profile.account_type = AccountType.DEALER.value
        self.test_dealer.save()

        self.client = Client()

        self.street = '456 Any Street'
        self.city = 'State College'
        self.state = 'PA'
        self.zip_code = 16870

        make = VehicleMake.objects.create(name='Volvo', website='www.volvo.com')
        make.save()
        self.make = make

    # check to see if the page shows the correct rendered form for a dealer
    def test_profile_edit_page_present_shopper(self):
        # user needs to be logged in to see the page
        self.client.force_login(self.test_dealer)

        response = self.client.get('/accounts/profile/edit/')
        self.assertContains(response, text='Vehicle Make Sold')

    # check to see if the page shows the correct rendered form for a shopper
    def test_profile_edit_page_present_dealer(self):
        # user needs to be logged in to see the page
        self.client.force_login(self.test_shopper)

        response = self.client.get('/accounts/profile/edit/')
        self.assertNotContains(response, text='Vehicle Make Sold')

    # check to see that an affiliation can be created
    def test_add_affiliation_to_dealer(self):
        affiliation = VehicleMake.objects.create(name="Ferrari", website='www.ferrari.com')

        self.test_dealer.profile.dealer_make = affiliation
        self.test_dealer.save()
        self.assertEqual(self.test_dealer.profile.dealer_make, affiliation)

    # check to see that an affiliation can be changed
    def test_change_affiliation_dealer(self):
        affiliation = VehicleMake.objects.create(name="Ferrari", website='www.ferrari.com')
        affiliation2 = VehicleMake.objects.create(name="Jeep", website='www.jeep.com')

        self.test_dealer.profile.dealer_make = affiliation
        self.test_dealer.save()
        self.assertEqual(self.test_dealer.profile.dealer_make, affiliation)

        self.test_dealer.profile.dealer_make = affiliation2
        self.test_dealer.save()
        self.assertEqual(self.test_dealer.profile.dealer_make, affiliation2)

    # test that the location edit form works as expected
    def test_profile_edit_affiliation_form_dealer(self):
        self.client.force_login(self.test_dealer)
        response = self.client.post(reverse('profile_edit'), data={
            'street': self.street,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'dealer_make': self.make.pk
        })

        make = User.objects.filter(username='testdealer')[0].profile.dealer_make

        self.assertEqual(make, self.make)


