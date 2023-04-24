"""
UserTestCase: A base test case class for tests that
require an authenticated user.

This class extends Django's TestCase and sets up a test user
during the test setup process.
By inheriting from this class, other test cases can easily
access an authenticated user for their tests.
"""

from django.test import TestCase
from django.contrib.auth.models import User


class UserTestCase(TestCase):
    """
    Set up a test user with a username and password for use in tests.
    This method is automatically called before running each test
    in a test case class.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
