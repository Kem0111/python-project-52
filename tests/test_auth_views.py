from django.test import TestCase
from tests.test_utils import BaseCRUDTest
from core.forms import LoginUserForm
from tests.test_utils import BaseTestCase
from django.urls import reverse


class LoginUserViewTest(BaseCRUDTest):

    def test_login_user_view_form_valid(self):
        response = self.client.post(
            "/login/", {"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("index"))


class LogoutUserViewTest(TestCase):

    def test_logout_user_view_redirects(self):
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("index"))


class LoginUserFormTest(BaseTestCase):

    def test_login_user_form_valid_data(self):
        form = LoginUserForm(
            data={"username": "testuser", "password": "testpassword"}
        )
        self.assertTrue(form.is_valid())

    def test_login_user_form_invalid_data(self):
        form = LoginUserForm(data={"username": "", "password": ""})
        self.assertFalse(form.is_valid())

    def test_login_user_view_form_valid(self):
        response = self.client.post(
            "/login/", {"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 302)
