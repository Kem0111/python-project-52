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
from typing import Dict, Optional, Type, Any, List
from django.db import models
from labels.models import Labels
from statuses.models import Statuses
from tasks.models import Tasks


class BaseTestCase(TestCase):
    """
    Set up a test user, status, task, label, with
    a username and password for use in tests.
    This method is automatically called before running each test
    in a test case class.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.status = Statuses.objects.create(name="teststatus")
        self.label = Labels.objects.create(name="testlabel")
        status_for_task = Statuses.objects.create(name="status_for_task")
        self.task = Tasks.objects.create(name='testtask',
                                         status=status_for_task,
                                         author=self.user)
        self.client.login(username="testuser", password="testpassword")


class BaseCRUDTest(BaseTestCase):
    """
    A base test case class for view tests that require an authenticated user.
    This class extends the UserTestCase and provides
    helper methods for testing CRUD.
    """

    def assertRendersCorrectTemplate(
            self, url: str, template_name: str, url_args:
            Optional[Dict[str, Any]] = None) -> None:
        """
        Asserts that the specified URL renders the correct template when
        accessed by an authenticated user.

        Args:
            url (str): The URL pattern name to test.
            template_name (str): The expected template name to be used.
            url_args (Optional[Dict[str, Any]]): Any URL arguments required for
            the URL pattern, default is None.
        """
        if url_args is None:
            url_args = {}
        response = self.client.get(reverse(url, kwargs=url_args))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)

    def assertRenderscorrectTemplateUnauthorized(
            self, url: str, template_name:
            str, url_args: Optional[Dict[str, Any]] = None) -> None:
        """
        Asserts that the specified URL does not render the given template when
        accessed by an unauthenticated user.

        Args:
            url (str): The URL pattern name to test.
            template_name (str): The template name that should not be used.
            url_args (Optional[Dict[str, Any]]): Any URL arguments required for
            the URL pattern, default is None.
        """
        if url_args is None:
            url_args = {}
        self.client.logout()
        response = self.client.get(reverse(url, kwargs=url_args))
        self.assertTemplateNotUsed(response, template_name)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("login"))

    def assertCreationViewFormValid(
            self, url: str, model: Type[models.Model],
            data: Dict[str, Any], revers_url: str) -> None:
        """
        Asserts that the specified creation view successfully creates an
        instance of the given model with valid form data.

        Args:
            url (str): The URL pattern name to test.
            model (Type[models.Model]): The model to test for a new instance.
            data (Dict[str, Any]): The form data to use
            for creating the instance.
            revers_url (str): The expected URL to redirect to
            after successful creation.
        """

        response = self.client.post(reverse(url), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(revers_url))
        created_data = model.objects.get(name=data['name'])
        self.assertEqual(created_data.name, data['name'])
        if len(data) > 1:
            self.assertEqual(created_data.status.pk, data['status'])
            self.assertEqual(created_data.description, data['description'])

    def assertCreationViewFormInValid(self, url: str, data: Dict[str, Any],
                                      template_name: str) -> None:
        """
        Asserts that the specified creation view returns an error
        when provided with invalid form data.

        Args:
            url (str): The URL pattern name to test.
            data (Dict[str, Any]): The invalid form data to use for testing.
            template_name (str): The expected template name to be used
            when rendering the error.
        """

        response = self.client.post(reverse(url), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)

    def assertUpdatedViewFormValid(self, url: str, args: List[Any], data:
                                   Dict[str, Any], reves_url: str) -> None:
        """
        Asserts that the specified update view successfully updates an
        instance with valid form data.

        Args:
            url (str): The URL pattern name to test.
            args (List[Any]): The arguments required for the URL pattern.
            data (Dict[str, Any]): The form data to use for
            updating the instance.
            reves_url (str): The expected URL to redirect to after
            successful update.
        """
        response = self.client.post(reverse(url, args=args), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(reves_url))

    def assertUpdatedViewFormInValid(self, url: str, args: List[Any], data:
                                     Dict[str, Any],
                                     template_name: str) -> None:
        """
        Asserts that the specified update view returns an error when
        provided with invalid form data.

        Args:
            url (str): The URL pattern name to test.
            args (List[Any]): The arguments required for the URL pattern.
            data (Dict[str, Any]): The invalid form data to use for testing.
            template_name (str): The expected template name to be used when
            rendering the error.
        """
        response = self.client.post(reverse(url, args=args), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name)

    def assertDeleteView(self, url: str, model: Type[models.Model],
                         revers_url: str,
                         args: int) -> None:
        """
        Assert that a delete view successfully deletes an object.

        This method tests that a delete view successfully deletes the object
        specified by `test_item` and redirects to the given `revers_url`.
        It also checks if the object has been removed from the database.

        Parameters:
        url (str): The URL pattern name of the delete view to test.
        model (Type[models.Model]): The model class of the object to be deleted.
        revers_url (str): The URL pattern name to which the view should
        redirect after successful deletion.
        test_item (Type[models.Model]): The instance of the object to be
        deleted.

        Returns:
        None
        """
        response = self.client.post(reverse(url, args=[args]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(revers_url))
        with self.assertRaises(model.DoesNotExist):
            model.objects.get(pk=args)
