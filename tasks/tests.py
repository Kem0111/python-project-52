from common.test_utils import BaseViewTest
from django.test import TestCase
from django.urls import reverse
from .models import Tasks
from .forms import TaskFilterForm
from statuses.models import Statuses
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from labels.models import Labels
# Create your tests here.


class TaskFilterFormTest(TestCase):

    def test_form_fields(self):
        form = TaskFilterForm()
        self.assertIn('status', form.fields)
        self.assertIn('executor', form.fields)
        self.assertIn('label', form.fields)
        self.assertIn('my_tasks_only', form.fields)


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
        test_status = Statuses.objects.create(name=_("teststatus"))
        data = {
            "name": "testtask",
            "description": "testdescription",
            "status": test_status.pk
        }
        self.assertCreationViewFormValid("create_task", Tasks, data, "tasks")
        created_task = Tasks.objects.get(name=data['name'])
        self.assertEqual(created_task.status, test_status)
        self.assertEqual(created_task.description, "testdescription")

    def test_creat_task_view_invalid_form(self):
        data = {
            "name": "testtask",
            "description": "testdescription"
        }
        self.assertCreationViewFormInValid("create_task", data,
                                           "tasks/create_task.html")


class UpdateTaskView(BaseViewTest):

    def test_tasks_view_render_template_test(self):
        test_task = self._create_test_task()
        self.assertRendersCorrectTemplate("update_task",
                                          'tasks/update_task.html',
                                          url_args={"pk": test_task.pk})

    def test_tasks_view_render_template_by_unlogin_user_test(self):
        test_task = self._create_test_task()
        self.assertRenderscorrectTemplateUnauthorized(
            "update_task",
            'tasks/update_task.html',
            url_args={"pk": test_task.pk}
        )

    def test_update_task_view_valid_form(self):

        test_task = self._create_test_task()
        test_status = Statuses.objects.create(name="teststatus2")
        data = {
            "name": "testtask2",
            "description": "testdescription2",
            "status": test_status.pk
        }
        self.assertUpdatedViewFormValid("update_task", [test_task.pk],
                                        data, "tasks")
        updated_task = Tasks.objects.get(name="testtask2")
        self.assertEqual(updated_task.name, "testtask2")
        assert test_task.pk == updated_task.pk
        self.assertEqual(updated_task.status, test_status)
        self.assertEqual(updated_task.description, "testdescription2")

    def test_update_task_view_invalid_form(self):
        test_task = self._create_test_task()
        data = {
            "name": "testtask2",
            "description": "testdescription2"
        }
        self.assertUpdatedViewFormInValid("update_task", [test_task.pk],
                                          data, 'tasks/update_task.html')


class DeleteTaskView(BaseViewTest):

    def test_delete_task_view_renders_correct_template(self):
        test_task = self._create_test_task()
        self.assertRendersCorrectTemplate("delete_task",
                                          "tasks/delete_task.html",
                                          url_args={"pk": test_task.pk})

    def test_delete_task_renders_correct_template_by_unlogin_user(self):
        test_task = self._create_test_task()
        self.assertRendersCorrectTemplate("delete_task",
                                          "tasks/delete_task.html",
                                          url_args={"pk": test_task.pk})

    def test_delete_task_view(self):
        test_task = self._create_test_task()
        self.assertDeleteView('delete_task', Tasks, 'tasks', test_task)


class TaskViewTest(BaseViewTest):

    def test_task_view_render_template_test(self):
        test_task = self._create_test_task()
        self.assertRendersCorrectTemplate("task_view",
                                          'tasks/task_view.html',
                                          url_args={"pk": test_task.pk})

    def test_task_view_render_template_by_unlogin_user(self):
        test_task = self._create_test_task()
        self.assertRenderscorrectTemplateUnauthorized(
            "task_view",
            'tasks/task_view.html',
            url_args={"pk": test_task.pk}
        )


class FilteredTasksViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')
        self.status = Statuses.objects.create(name='Test Status')
        self.label = Labels.objects.create(name='Test Label')
        self.task = Tasks.objects.create(
            name='Test Task',
            status=self.status,
            author=self.user,
            executor=self.user
        )
        self.task.labels.add(self.label)

    def test_filters(self):
        self.client.login(username='testuser', password='testpassword')

        filter_tests = [
            ('status', self.status.pk),
            ('executor', self.user.pk),
            ('label', self.label.pk),
            ('my_tasks_only', 'on')
        ]

        for filter_key, filter_value in filter_tests:
            with self.subTest(filter=filter_key):
                response = self.client.get(reverse('tasks'),
                                           {filter_key: filter_value})
                self.assertEqual(response.status_code, 200)
                self.assertQuerysetEqual(response.context['object_list'],
                                         [self.task])
