from django.urls import reverse
from django.test import TestCase, RequestFactory
from users.views import RegistrationUserView
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import User


class RegistrationUserViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.message_middleware = MessageMiddleware(lambda req: None)
        self.session_middleware = SessionMiddleware(lambda req: None)

    def test_registration_user_view_renders_correct_template(self):
        response = self.client.get(reverse("register"))
        self.assertTemplateUsed(response, "users/register.html")

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


class UsersViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_users_view_renders_correct_template(self):
        response = self.client.get(reverse("users"))
        self.assertTemplateUsed(response, "users/index.html")


class UpdateUserViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')

    def test_update_user_view_renders_correct_template(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('update_user', args=[self.user.pk]))
        self.assertTemplateUsed(response, 'users/update.html')

    def test_update_user_view_form_valid(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse("update_user",
                                            args=[self.user.pk]), {
            "first_name": "Updated",
            "last_name": "User",
            "username": 'testuser'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "User")


class UserPasswordChangeViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')

    def test_user_password_view_renders_correct_template(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('change_password',
                                           args=[self.user.pk]))
        self.assertTemplateUsed(response, 'users/change_password.html')

    def test_user_password_view_form_valid(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('change_password',
                                            args=[self.user.pk]), {
            'old_password': 'testpassword',
            'new_password1': 'updatepassword',
            'new_password2': 'updatepassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users'))

    def test_user_password_view_form_invalid(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('change_password',
                                            args=[self.user.pk]), {
            'old_password': 'testpassword',
            'new_password1': 'updatepassword',
            'new_password2': 'updatepasswordqwe'
        })
        self.assertEqual(response.status_code, 200)


class DeleteUserViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')

    def delete_user_view_test(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('delete_user', args=[self.user.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'index.html')
        self.user.refresh_from_db()
        not self.assertEqual(self.user.pk, 'pk')
