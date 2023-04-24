from django.urls import reverse
from .models import Statuses
from common.test_utils import UserTestCase
# Create your tests here.


class StatusesViewTest(UserTestCase):

    def test_users_view_renders_correct_template(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse("statuses"))
        self.assertTemplateUsed(response, "statuses/index.html")


class CreateStatusViewTest(UserTestCase):

    def test_create_status_view_renders_correct_template(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse("create_status"))
        self.assertTemplateUsed(response, 'statuses/create_status.html')

    def test_creation_status_view_form_valid(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse("create_status"), {
            'name': 'Created'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('statuses'))
        created_status = Statuses.objects.get(name='Created')
        self.assertEqual(created_status.name, 'Created')

    def test_creation_status_view_form_invalid(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('create_status'), {
            'name': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/create_status.html')


class DeleteStatusViewTest(UserTestCase):

    def test_deleted_status_view(self):
        self.client.login(username='testuser', password='testpassword')
        self.status = Statuses.objects.create(name="Created")
        response = self.client.post(reverse('delete_status',
                                            args=[self.status.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('statuses'))
        with self.assertRaises(Statuses.DoesNotExist):
            self.status.refresh_from_db()
        self.assertNotEqual(self.status.pk, 'pk')


class UpdateStatusViewTest(UserTestCase):

    def test_updated_status_view_form_valid(self):
        self.client.login(username='testuser', password='testpassword')
        self.status = Statuses.objects.create(name="Created")
        response = self.client.post(reverse('update_status',
                                            args=[self.status.pk]), {
            'name': 'Updated'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("statuses"))
        updated_status = Statuses.objects.get(name='Updated')
        assert updated_status.pk == self.status.pk
        self.assertEqual(updated_status.name, 'Updated')

    def test_updated_status_view_form_invalid(self):
        self.client.login(username='testuser', password='testpassword')
        self.status = Statuses.objects.create(name="Created")
        response = self.client.post(reverse('update_status',
                                            args=[self.status.pk]), {
            'name': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/update_status.html')
