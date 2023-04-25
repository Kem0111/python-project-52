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
from django.urls import reverse


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


class BaseViewTest(UserTestCase):

    def assertRendersCorrectTemplate(self, url, template_name, url_args=None):
        if url_args is None:
            url_args = {}
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse(url, kwargs=url_args))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)

    def assertRenderscorrectTemplateUnauthorized(self, url, template_name,
                                                 url_args=None):
        if url_args is None:
            url_args = {}
        response = self.client.get(reverse(url, kwargs=url_args))
        self.assertTemplateNotUsed(response, template_name)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("login"))
