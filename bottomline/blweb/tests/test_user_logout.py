from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client


# Test class for unit tests on the user login interface
class TestUserLogout(TestCase):

    # any needed setup for the tests. this function will be run before every test case
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='test@#628password')
        test_user.save()
        self.client = Client()
        self.client.login(username='baduser', password='test@#628password')

    # check to see if the page is present
    def test_logout_page_present(self):
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 200)

    # check that a user can log out
    def test_user_log_out_success(self):
        response = self.client.get('/accounts/logout/')
        response = self.client.get('/accounts/profile/')
        self.assertNotEqual(response.status_code, HTTPStatus.OK)



