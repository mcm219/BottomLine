from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from django.urls import reverse


# Test class for unit tests on the user login interface
from blweb.models import AccountType


class TestAccountCreate(TestCase):

    # any needed setup for the tests. this function will be run before every test case
    def setUp(self):
        self.client = Client()
        self.username = "TEST_USER_123"
        self.first_name = "TEST"
        self.last_name = "USER"
        self.email = "TEST@host.com"
        self.phone = "(912) 123-4567"
        self.password1 = "rqwerwfw12321ef"

    # check to see if the shopper page is present
    def test_account_create_page_present(self):
        response = self.client.get('/accounts/account_signup/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='account_signup.html')

    # check that the proper view was used (shopper)
    def test_account_view_name(self):
        response = self.client.get(reverse('account_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='account_signup.html')

    # check to see if the dealer page is present
    def test_dealer_account_create_page_present(self):
        response = self.client.get('/accounts/dealer_signup/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='dealer_signup.html')

    # check that the proper view was used (dealer)
    def test_dealer_account_view_name(self):
        response = self.client.get(reverse('dealer_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='dealer_signup.html')

    # test that the user signup form works as expected
    def test_shopper_account_form(self):
        response = self.client.post(reverse('account_signup'), data={
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'email': self.email,
            'password1': self.password1,
            'password2': self.password1
        })
        self.assertEqual(response.status_code, 200)

        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)

    # test that the account_type is set correctly for a dealer
    def test_shopper_account_type(self):
        response = self.client.post(reverse('account_signup'), data={
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'email': self.email,
            'password1': self.password1,
            'password2': self.password1
        })

        user = User.objects.get(username=self.username)
        self.assertEqual(AccountType.SHOPPER.value, user.profile.account_type)

    # test that the dealer signup form works as expected
    def test_dealer_account_form(self):
        response = self.client.post(reverse('dealer_signup'), data={
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'email': self.email,
            'password1': self.password1,
            'password2': self.password1
        })
        self.assertEqual(response.status_code, 200)

        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)

    # test that the account_type is set correctly for a dealer
    def test_dealer_account_type(self):
        response = self.client.post(reverse('dealer_signup'), data={
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'email': self.email,
            'password1': self.password1,
            'password2': self.password1
        })

        user = User.objects.get(username=self.username)
        self.assertEqual(AccountType.DEALER.value, user.profile.account_type)

