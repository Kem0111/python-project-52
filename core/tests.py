from django.test import TestCase
from core.forms import LoginUserForm
from common.test_utils import UserTestCase


class HomePageViewTest(TestCase):

    def test_home_page_view_renders_correct_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "index.html")


class LoginUserViewTest(UserTestCase):

    def test_login_user_view_renders_correct_template(self):
        response = self.client.get("/login/")
        self.assertTemplateUsed(response, "login.html")

    def test_login_user_view_form_valid(self):
        response = self.client.post(
            "/login/", {"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 302)


class LogoutUserViewTest(TestCase):

    def test_logout_user_view_redirects(self):
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 302)


class LoginUserFormTest(UserTestCase):

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
