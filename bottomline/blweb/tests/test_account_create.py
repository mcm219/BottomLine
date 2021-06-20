from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client


# Test class for unit tests on the user login interface
class TestAccountCreate(TestCase):

    # any needed setup for the tests. this function will be run before every test case
    def setUp(self):
        self.client = Client()

    # check to see if the shopper page is present
    def test_account_create_page_present(self):
        response = self.client.get('/accounts/account_signup/')
        self.assertEqual(response.status_code, 200)

    # check to see if the dealer page is present
    def test_dealer_account_create_page_present(self):
        response = self.client.get('/accounts/dealer_signup/')
        self.assertEqual(response.status_code, 200)

