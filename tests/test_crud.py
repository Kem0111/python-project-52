from tests.test_utils import BaseCRUDTest
from labels.models import Labels
from statuses.models import Statuses
from tasks.models import Tasks
from django.contrib.auth.models import User


class ReadViewsTest(BaseCRUDTest):

    def setUp(self):
        super().setUp()

        self.app_template_view_for_authorized_user_params = [
            ("tasks", 'tasks/index.html'),
            ("task_view", 'tasks/task_view.html', {"pk": self.task.pk}),
            ("create_task", 'tasks/create_task.html'),
            ("update_task", 'tasks/update_task.html', {"pk": self.task.pk}),
            ("delete_task", "tasks/delete_task.html", {"pk": self.task.pk}),
            ("labels", "labels/index.html"),
            ("create_label", "labels/create_label.html"),
            ("update_label", "labels/update_label.html", {"pk": self.label.pk}),
            ("delete_label", "labels/delete_label.html", {"pk": self.label.pk}),
            ("statuses", "statuses/index.html"),
            ("create_status", "statuses/create_status.html"),
            ('update_user', 'users/update.html', {"pk": self.user.pk}),
            (
                "update_status", "statuses/update_status.html",
                {"pk": self.status.pk}
            ),
            (
                "delete_status", "statuses/delete_status.html",
                {"pk": self.status.pk}
            ),
            (
                'change_password', 'users/change_password.html',
                {"pk": self.user.pk}
            )
        ]
        self.all_app_template_view_params = (
            self.app_template_view_for_authorized_user_params + [
                ("index", "index.html"),
                ("login", "login.html"),
                ("register", "users/register.html"),
                ("users", "users/index.html")
            ]
        )

    def test_app_view_renders_correct_template(self):
        for params in self.all_app_template_view_params:
            self.assertRendersCorrectTemplate(*params)

    def test_app_view_renders_correct_template_by_unlogin_user(self):
        for params in self.app_template_view_for_authorized_user_params:
            self.assertRenderscorrectTemplateUnauthorized(*params)


class CreateViewsTest(BaseCRUDTest):

    def setUp(self):
        super().setUp()

        self.task_data = {
            "name": "newtesttask",
            "description": "testdescription",
            "status": self.status.pk,
        }
        self.app_create_view_correct_params = [
            ("create_task", Tasks, self.task_data, "tasks"),
            ("create_label", Labels, {"name": "Created_label"}, "labels"),
            ("create_status", Statuses, {"name": "Created_statuss"}, "statuses")
        ]
        self.app_create_view_incorrect_params = [
            ("create_task", {"name": "new_name"}, "tasks/create_task.html"),
            ("create_label", {"name": ""}, "labels/create_label.html"),
            ("create_status", {"name": ""}, "statuses/create_status.html")
        ]

    def test_create_view_form_valid(self):
        for params in self.app_create_view_correct_params:
            self.assertCreationViewFormValid(*params)

    def test_create_view_form_invalid(self):
        for params in self.app_create_view_incorrect_params:
            self.assertCreationViewFormInValid(*params)


class UpdateViewsTest(BaseCRUDTest):

    def setUp(self):
        super().setUp()
        self.correct_data = {
            "task": {
                "name": "updatetask",
                "description": "updatedescription",
                "status": self.status.pk
            },
            "user": {
                "first_name": "Updated",
                "last_name": "User",
                "username": "testuser"
            },
            "label": {"name": "updated_label"},
            "status": {"name": "updated_status"},
            "password": {
                'old_password': 'testpassword',
                'new_password1': 'updatepassword',
                'new_password2': 'updatepassword'
            }
        }
        self.incorrect_data = {
            "task": {
                "name": "updatetask",
                "description": "updatedescription",
            },
            "user": {
                "first_name": "Updated",
                "last_name": "User",
                "username": ""
            },
            "label": {"name": ""},
            "status": {"name": ""},
            "password": {
                'old_password': 'testpassword',
                'new_password1': 'update',
                'new_password2': 'updatepassword'
            }
        }
        self.base_params = [
            (
                "update_task", self.task.pk,
                "tasks/update_task.html", self.correct_data["task"],
                self.incorrect_data["task"], "tasks"
            ),
            (
                "update_label", self.label.pk,
                "labels/update_label.html", self.correct_data["label"],
                self.incorrect_data["label"], "labels"
            ),
            (
                "update_status", self.status.pk,
                "statuses/update_status.html", self.correct_data["status"],
                self.incorrect_data["status"], "statuses"
            ),
            (
                "update_user", self.user.pk,
                "users/update.html", self.correct_data["user"],
                self.incorrect_data["user"], "users"),
            (
                'change_password', self.user.pk,
                'users/change_password.html', self.correct_data["password"],
                self.incorrect_data["password"], 'users'
            ),
        ]

        self.app_update_view_correct_params = [
            (view_name, [item_pk], data, revers_view)
            for view_name, item_pk, _, data, _, revers_view in self.base_params
        ]
        self.app_update_view_incorrect_params = [
            (view_name, [item_pk], data, template)
            for view_name, item_pk, template, _, data, _ in self.base_params
        ]

    def test_update_view_form_valid(self):
        for params in self.app_update_view_correct_params:
            self.assertUpdatedViewFormValid(*params)

    def test_update_view_form_invalid(self):
        for params in self.app_update_view_incorrect_params:
            self.assertUpdatedViewFormInValid(*params)


class DeleteViewsTest(BaseCRUDTest):

    def setUp(self):
        super().setUp()
        self.app_delete_view_correct_params = [
            ('delete_task', Tasks, 'tasks', self.task.pk),
            ('delete_label', Labels, 'labels', self.label.pk),
            ('delete_status', Statuses, 'statuses', self.status.pk),
            ('delete_user', User, 'index', self.user.pk)
        ]

    def test_delete_view_form_valid(self):
        for params in self.app_delete_view_correct_params:
            self.assertDeleteView(*params)
