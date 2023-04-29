from django.urls import reverse
from django.test import RequestFactory
from users.views import RegistrationUserView
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from tests.test_utils import BaseCRUDTest


class RegistrationUserViewTest(BaseCRUDTest):

    def setUp(self):
        self.factory = RequestFactory()
        self.message_middleware = MessageMiddleware(lambda req: None)
        self.session_middleware = SessionMiddleware(lambda req: None)

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
