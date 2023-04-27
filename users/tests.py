from django.urls import reverse
from django.test import RequestFactory
from users.views import RegistrationUserView
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from common.test_utils import BaseViewTest


class RegistrationUserViewTest(BaseViewTest):

    def setUp(self):
        self.factory = RequestFactory()
        self.message_middleware = MessageMiddleware(lambda req: None)
        self.session_middleware = SessionMiddleware(lambda req: None)

    def test_registration_user_view_renders_correct_template(self):
        self.assertRendersCorrectTemplate("register", "users/register.html")

    def test_registration_user_view_form_valid(self):

        request = self.factory.post(reverse("register"), {
            "first_name": "Test",
            "last_name": "Test",
            "username": "newuser",
            "password1": "testpassword",
            "password2": "testpassword",
        })
        self.session_middleware.process_request(request)
        self.message_middleware.process_request(request)
        request.user = AnonymousUser()
        response = RegistrationUserView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("login"))

    def test_registration_user_view_form_invalid(self):
        request = self.factory.post(reverse("register"), {
            "username": "newuser",
            "password1": "testpassword",
            "password2": "differentpassword",
        })
        self.session_middleware.process_request(request)
        self.message_middleware.process_request(request)
        request.user = AnonymousUser()
        response = RegistrationUserView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class UsersViewTest(BaseViewTest):

    def test_users_view_renders_correct_template(self):
        self.assertRendersCorrectTemplate("users", "users/index.html")


class UpdateUserViewTest(BaseViewTest):

    def test_update_user_view_renders_correct_template(self):
        self.assertRendersCorrectTemplate('update_user',
                                          'users/update.html',
                                          url_args={"pk": self.user.pk})

    def test_update_user_view_renders_correct_template_by_unlogin_user(self):
        self.assertRenderscorrectTemplateUnauthorized(
            'update_user',
            'users/update.html',
            url_args={"pk": self.user.pk}
        )

    def test_update_user_view_form_valid(self):
        data = {
            "first_name": "Updated",
            "last_name": "User",
            "username": 'testuser'
        }
        self.assertUpdatedViewFormValid("update_user", [self.user.pk],
                                        data, "users")
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "User")


class UserPasswordChangeViewTest(BaseViewTest):

    def test_user_password_view_renders_correct_template(self):
        self.assertRendersCorrectTemplate('change_password',
                                          'users/change_password.html',
                                          url_args={"pk": self.user.pk})

    def test_user_password_view_renders_correct_template_by_unlogin_user(self):
        self.assertRenderscorrectTemplateUnauthorized(
            'change_password',
            'users/change_password.html',
            url_args={"pk": self.user.pk}
        )

    def test_user_password_view_form_valid(self):
        data = {
            'old_password': 'testpassword',
            'new_password1': 'updatepassword',
            'new_password2': 'updatepassword'
        }
        self.assertUpdatedViewFormValid('change_password', [self.user.pk],
                                        data, 'users')
        self.user.refresh_from_db()
        self.assertTrue(check_password('updatepassword', self.user.password))

    def test_user_password_view_form_invalid(self):
        data = {
            'old_password': 'testpassword',
            'new_password1': 'password',
            'new_password2': 'another'
        }
        self.assertUpdatedViewFormInValid('change_password', [self.user.pk],
                                          data, 'users/change_password.html')


class DeleteUserViewTest(BaseViewTest):

    def delete_user_view_test(self):
        self.assertDeleteView('delete_user', User, 'index', [self.user.pk])
