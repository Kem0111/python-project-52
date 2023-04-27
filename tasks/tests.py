from django.test import TestCase
from django.urls import reverse
from .models import Tasks
from .forms import TaskFilterForm
from statuses.models import Statuses
from django.contrib.auth.models import User
from labels.models import Labels
# Create your tests here.


class TaskFilterFormTest(TestCase):

    def test_form_fields(self):
        form = TaskFilterForm()
        self.assertIn('status', form.fields)
        self.assertIn('executor', form.fields)
        self.assertIn('label', form.fields)
        self.assertIn('my_tasks_only', form.fields)


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
