from django.urls import reverse
from .models import Labels
from common.test_utils import BaseViewTest
# Create your tests here.


class LabelsViewTest(BaseViewTest):

    def test_labels_view_renders_correct_template(self):
        self.assertRendersCorrectTemplate("labels",
                                          "labels/index.html")

    def test_labels_view_renders_correct_template_by_unlogin_user(self):
        self.assertRenderscorrectTemplateUnauthorized("labels",
                                                      "label/index.html")


class CreateLabelViewTest(BaseViewTest):

    def test_create_label_view_renders_correct_template(self):
        self.assertRendersCorrectTemplate("create_label",
                                          "labels/create_label.html")

    def test_create_label_renders_correct_template_by_unlogin_user(self):
        self.assertRenderscorrectTemplateUnauthorized(
            "create_label",
            "labels/create_label.html"
        )

    def test_creation_label_view_form_valid(self):
        data = {'name': 'Created_label'}
        self.assertCreationViewFormValid("create_label", Labels, data, 'labels')

    def test_creation_label_view_form_invalid(self):
        data = {'name': ''}
        self.assertCreationViewFormInValid(
            'create_label', data,
            'labels/create_label.html'
        )


class DeleteLabelViewTest(BaseViewTest):

    def test_delete_label_view_renders_correct_template(self):
        test_label = Labels.objects.create(name="testlabel")
        self.assertRendersCorrectTemplate("delete_label",
                                          "labels/delete_label.html",
                                          url_args={"pk": test_label.pk})

    def test_delete_label_renders_correct_template_by_unlogin_user(self):
        test_label = Labels.objects.create(name="testlabel")
        self.assertRenderscorrectTemplateUnauthorized(
            "delete_label",
            "labels/delete_label.html",
            url_args={"pk": test_label.pk}
        )

    def test_deleted_label_view(self):
        self.client.login(username='testuser', password='testpassword')
        self.label = Labels.objects.create(name="Created")
        response = self.client.post(reverse('delete_label',
                                            args=[self.label.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('labels'))
        with self.assertRaises(Labels.DoesNotExist):
            self.label.refresh_from_db()
        self.assertNotEqual(self.label.pk, 'pk')


class UpdatelabelViewTest(BaseViewTest):

    def test_update_label_view_renders_correct_template(self):
        test_label = self._create_test_label()
        self.assertRendersCorrectTemplate("update_label",
                                          "labels/update_label.html",
                                          url_args={"pk": test_label.pk})

    def test_update_label_renders_correct_template_by_unlogin_user(self):
        test_label = self._create_test_label()
        self.assertRenderscorrectTemplateUnauthorized(
            "update_label",
            "labels/update_label.html",
            url_args={"pk": test_label.pk}
        )

    def test_updated_label_view_form_valid(self):
        test_label = self._create_test_label()
        data = {'name': 'Updated_label'}
        self.assertUpdatedViewFormValid('update_label', [test_label.pk],
                                        data, "labels")
        updated_label = Labels.objects.get(name='Updated_label')
        self.assertEqual(updated_label.name, 'Updated_label')
        assert updated_label.pk == test_label.pk

    def test_updated_label_view_form_invalid(self):
        test_label = self._create_test_label()
        data = {
            'name': ''
        }
        self.assertUpdatedViewFormInValid('update_label', [test_label.pk],
                                          data, 'labels/update_label.html')
