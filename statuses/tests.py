from django.urls import reverse
from .models import Statuses
from common.test_utils import BaseViewTest
# Create your tests here.


class StatusesViewTest(BaseViewTest):

    def test_statuses_view_renders_correct_template(self):
        self.assertRendersCorrectTemplate("statuses",
                                          "statuses/index.html")

    def test_statuses_view_renders_correct_template_by_unlogin_user(self):
        self.assertRenderscorrectTemplateUnauthorized(
            "statuses",
            "statuses/index.html"
        )


class CreateStatusViewTest(BaseViewTest):

    def test_create_status_view_renders_correct_template(self):
        self.assertRendersCorrectTemplate("create_status",
                                          "statuses/create_status.html")

    def test_create_status_renders_correct_template_by_unlogin_user(self):
        self.assertRenderscorrectTemplateUnauthorized(
            "create_status",
            "statuses/create_status.html"
        )

    def test_creation_status_view_form_valid(self):
        data = {'name': 'Created_status'}
        self.assertCreationViewFormValid("create_status", Statuses,
                                         data, 'statuses')

    def test_creation_status_view_form_invalid(self):
        data = {'name': ''}
        self.assertCreationViewFormInValid('create_status', data,
                                           'statuses/create_status.html')


class DeleteStatusViewTest(BaseViewTest):

    def test_delete_status_view_renders_correct_template(self):
        test_status = Statuses.objects.create(name="teststatus")
        self.assertRendersCorrectTemplate("delete_status",
                                          "statuses/delete_status.html",
                                          url_args={"pk": test_status.pk})

    def test_delete_status_renders_correct_template_by_unlogin_user(self):
        test_status = Statuses.objects.create(name="teststatus")
        self.assertRenderscorrectTemplateUnauthorized(
            "delete_status",
            "statuses/delete_status.html",
            url_args={"pk": test_status.pk}
        )

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


class UpdateStatusViewTest(BaseViewTest):

    def test_update_status_view_renders_correct_template(self):
        test_status = Statuses.objects.create(name="teststatus")
        self.assertRendersCorrectTemplate("update_status",
                                          "statuses/update_status.html",
                                          url_args={"pk": test_status.pk})

    def test_update_status_renders_correct_template_by_unlogin_user(self):
        test_status = Statuses.objects.create(name="teststatus")
        self.assertRenderscorrectTemplateUnauthorized(
            "update_status",
            "statuses/update_status.html",
            url_args={"pk": test_status.pk}
        )

    def test_updated_status_view_form_valid(self):
        test_status = Statuses.objects.create(name="Created")
        data = {'name': 'Updated_status'}
        self.assertUpdatedViewFormValid('update_status', [test_status.pk],
                                        data, "statuses")
        updated_status = Statuses.objects.get(name='Updated_status')
        self.assertEqual(updated_status.name, 'Updated_status')
        assert updated_status.pk == test_status.pk

    def test_updated_status_view_form_invalid(self):
        test_status = Statuses.objects.create(name="Created")
        data = {
            'name': ''
        }
        self.assertUpdatedViewFormInValid('update_status', [test_status.pk],
                                          data, 'statuses/update_status.html')
