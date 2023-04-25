from common.test_utils import BaseViewTest
from django.test import TestCase
from django.urls import reverse
from .models import Tasks
from statuses.models import Statuses
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
# Create your tests here.


class CreateTestTask(TestCase):

    def _create_task(self):
        user = User.objects.get(username="testuser")
        test_status = Statuses.objects.create(name="teststatus")
        test_task = Tasks.objects.create(name='testtask', status=test_status,
                                         author=user)
        return test_task


class TasksViewTest(BaseViewTest):

    def test_tasks_view_render_template_test(self):
        self.assertRendersCorrectTemplate("tasks", 'tasks/index.html')

    def test_tasks_view_render_template_by_unlogin_user(self):
        self.assertRenderscorrectTemplateUnauthorized("tasks",
                                                      'tasks/index.html')


class CreateTaskView(BaseViewTest):

    def test_tasks_view_render_template_test(self):
        self.assertRendersCorrectTemplate("create_task",
                                          'tasks/create_task.html')

    def test_tasks_view_render_template_by_unlogin_user_test(self):
        self.assertRenderscorrectTemplateUnauthorized(
            "create_task", 'tasks/create_task.html'
        )

    def test_creat_task_view_valid_form(self):
        self.client.login(username="testuser", password="testpassword")
        test_status = Statuses.objects.create(name=_("teststatus"))
        response = self.client.post(reverse("create_task"), {
            "name": "testtask",
            "description": "testdescription",
            "status": test_status.pk
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("tasks"))
        created_task = Tasks.objects.get(name="testtask")
        self.assertEqual(created_task.name, "testtask")
        self.assertEqual(created_task.status, test_status)
        self.assertEqual(created_task.description, "testdescription")

    def test_creat_task_view_invalid_form(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse("create_task"), {
            "name": "testtask",
            "description": "testdescription",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/create_task.html")


class UpdateTaskView(BaseViewTest, CreateTestTask):

    def test_tasks_view_render_template_test(self):
        test_task = self._create_task()
        self.assertRendersCorrectTemplate("update_task",
                                          'tasks/update_task.html',
                                          url_args={"pk": test_task.pk})

    def test_tasks_view_render_template_by_unlogin_user_test(self):
        test_task = self._create_task()
        self.assertRenderscorrectTemplateUnauthorized(
            "update_task",
            'tasks/update_task.html',
            url_args={"pk": test_task.pk}
        )

    def test_update_task_view_valid_form(self):

        test_task = self._create_task()
        self.client.login(username="testuser", password="testpassword")
        test_status = Statuses.objects.create(name="teststatus2")
        response = self.client.post(reverse("update_task",
                                            args=[test_task.pk]), {
            "name": "testtask2",
            "description": "testdescription2",
            "status": test_status.pk
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("tasks"))
        updated_task = Tasks.objects.get(name="testtask2")
        self.assertEqual(updated_task.name, "testtask2")
        self.assertEqual(updated_task.status, test_status)
        self.assertEqual(updated_task.description, "testdescription2")

    def test_update_task_view_invalid_form(self):
        test_task = self._create_task()
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse("update_task",
                                            args=[test_task.pk]), {
            "name": "testtask2",
            "description": "testdescription2",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/update_task.html')


class DeleteTaskView(BaseViewTest, CreateTestTask):

    def test_delete_task_view_renders_correct_template(self):
        test_task = self._create_task()
        self.assertRendersCorrectTemplate("delete_task",
                                          "tasks/delete_task.html",
                                          url_args={"pk": test_task.pk})

    def test_delete_task_renders_correct_template_by_unlogin_user(self):
        test_task = self._create_task()
        self.assertRendersCorrectTemplate("delete_task",
                                          "tasks/delete_task.html",
                                          url_args={"pk": test_task.pk})

    def test_delete_task_view(self):
        self.client.login(username='testuser', password='testpassword')
        test_task = self._create_task()
        response = self.client.post(reverse('delete_task',
                                            args=[test_task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('tasks'))
        with self.assertRaises(Tasks.DoesNotExist):
            test_task.refresh_from_db()
        self.assertNotEqual(test_task.pk, 'pk')


class TaskViewTest(BaseViewTest, CreateTestTask):

    def test_task_view_render_template_test(self):
        test_task = self._create_task()
        self.assertRendersCorrectTemplate("task_view",
                                          'tasks/task_view.html',
                                          url_args={"pk": test_task.pk})

    def test_task_view_render_template_by_unlogin_user(self):
        test_task = self._create_task()
        self.assertRenderscorrectTemplateUnauthorized(
            "task_view",
            'tasks/task_view.html',
            url_args={"pk": test_task.pk}
        )
