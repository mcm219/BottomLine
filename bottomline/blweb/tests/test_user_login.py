from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client


# Test class for unit tests on the user login interface
class TestUserLogin(TestCase):

    # any needed setup for the tests. this function will be run before every test case
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='test@#628password')
        test_user.save()
        self.client = Client()

    # check to see if the page is present
    def test_login_page_present(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    # check that a user can log in
    def test_user_log_in_success(self):
        login = self.client.login(username='testuser', password='test@#628password')
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # check that bad credentials fail log in (user)
    def test_user_log_in_fail_user(self):
        login = self.client.login(username='baduser', password='test@#628password')
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    # check that bad credentials fail log in (password)
    def test_user_log_in_fail_password(self):
        login = self.client.login(username='testuser', password='1234BadPassword!!')
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    # check that a successful log in redirects to the profile page
    def test_user_login_profile_page(self):
        login = self.client.login(username='testuser', password='test@#628password')
        response = self.client.get('/accounts/profile/')
        self.assertContains(response, text="testuser")


