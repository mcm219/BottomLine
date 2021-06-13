from django.test import TestCase


# Test class for unit tests on the user login interface
class TestUserLogin(TestCase):

    # any needed setup for the tests. this function will be run before every test case
    def SetUp(self):
        pass

    # check to see if the page is present
    def test_login_page_present(self):
        pass

    # check that a user can log in
    def test_user_log_in_success(self):
        pass

    # check that bad credentials fail log in
    def test_user_log_in_fail(self):
        pass

    # check that a successful log in redirects to the profile page
    def test_user_login_profile_page(self):
        pass
