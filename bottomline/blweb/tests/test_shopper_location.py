from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client

# Test class for unit tests on the dealer location
from django.urls import reverse

from blweb.models import AccountType, Address


class TestShopperLocation(TestCase):

    # any needed setup for the tests. this function will be run before every test case
    def setUp(self):
        self.test_shopper = User.objects.create_user(username='testshopper', password='test@#628password')
        self.test_shopper.profile.account_type = AccountType.SHOPPER.value
        self.test_shopper.save()
        self.client = Client()

        self.street = '456 Any Street'
        self.city = 'State College'
        self.state = 'PA'
        self.zip_code = 16870

    # check to see if the page is present
    def test_profile_edit_page_present_shopper(self):
        # user needs to be logged in to see the page
        self.client.force_login(self.test_shopper)

        response = self.client.get('/accounts/profile/edit/')
        self.assertEqual(response.status_code, 200)

    # check that the proper view was used (dealer)
    def test_profile_edit_view_name_shopper(self):
        # user needs to be logged in to see the page
        self.client.force_login(self.test_shopper)

        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='profile_edit.html')

    # check to see that the Profile link is present on the landing page when logged in
    def test_profile_link_logged_in_shopper(self):
        # user needs to be logged in to see the page
        self.client.force_login(self.test_shopper)

        response = self.client.get(reverse('landing'))
        self.assertContains(response, text="Profile")

    # check to see that an address can be created
    def test_add_address_to_shopper(self):
        address = Address.objects.create(street='123 main street',
                                         city='Smallville',
                                         state='KS',
                                         zip_code='90210')

        self.test_shopper.profile.address = address
        self.test_shopper.save()
        self.assertEqual(self.test_shopper.profile.address.street, '123 main street')

    # check to see that the address can be updated
    def test_change_shopper_address(self):
        address = Address.objects.create(street='123 main street',
                                         city='Smallville',
                                         state='KS',
                                         zip_code='90210')

        self.test_shopper.profile.address = address
        self.test_shopper.save()
        self.assertEqual(self.test_shopper.profile.address.street, '123 main street')

        # now change the street
        address = Address.objects.create(street='100 Madison Ave',
                                         city='New York',
                                         state='NY',
                                         zip_code='90210')
        self.test_shopper.profile.address = address
        self.test_shopper.save()
        self.assertEqual(self.test_shopper.profile.address.city, 'New York')

    # test that the location edit form works as expected
    def test_profile_edit_address_form_shopper(self):
        self.client.force_login(self.test_shopper)
        response = self.client.post(reverse('profile_edit'), data={
            'street': self.street,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
        })

        address = User.objects.filter(username='testshopper')[0].profile.address

        self.assertEqual(address.city, self.city)
