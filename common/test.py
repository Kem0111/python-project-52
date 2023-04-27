from common.test_utils import BaseCRUDTest, ITEM_PK
from parameterized import parameterized
from labels.models import Labels
from statuses.models import Statuses
from tasks.models import Tasks


class ReadViewsTest(BaseCRUDTest):

    app_template_view_for_authorized_users_params = [
        ("tasks", 'tasks/index.html'),
        ("task_view", 'tasks/task_view.html', {"pk": ITEM_PK}),
        ("create_task", 'tasks/create_task.html'),
        ("update_task", 'tasks/update_task.html', {"pk": ITEM_PK}),
        ("delete_task", "tasks/delete_task.html", {"pk": ITEM_PK}),
        ("labels", "labels/index.html"),
        ("create_label", "labels/create_label.html"),
        ("update_label", "labels/update_label.html", {"pk": ITEM_PK}),
        ("delete_label", "labels/delete_label.html", {"pk": ITEM_PK}),
        ("statuses", "statuses/index.html"),
        ("create_status", "statuses/create_status.html"),
        ("update_status", "statuses/update_status.html", {"pk": ITEM_PK}),
        ("delete_status", "statuses/delete_status.html", {"pk": ITEM_PK}),
        ('change_password', 'users/change_password.html', {"pk": ITEM_PK}),
        ('update_user', 'users/update.html', {"pk": ITEM_PK})
    ]
    all_app_template_view_params = (
        app_template_view_for_authorized_users_params + [
            ("index", "index.html"),
            ("login", "login.html"),
            ("register", "users/register.html"),
            ("users", "users/index.html")
        ]
    )

    @parameterized.expand(all_app_template_view_params)
    def test_app_view_renders_correct_template(self, view_name,
                                               template_name, url_args=None):
        self.assertRendersCorrectTemplate(view_name, template_name, url_args)

    @parameterized.expand(app_template_view_for_authorized_users_params)
    def test_app_view_renders_correct_template_by_unlogin_user(
            self, view_name,
            template_name, url_args=None
    ):
        self.assertRenderscorrectTemplateUnauthorized(view_name, template_name,
                                                      url_args)


class CreateViewsTest(BaseCRUDTest):

    task_data = {
        "name": "newtesttask",
        "description": "testdescription",
        "status": ITEM_PK,
    }

    app_create_view_correct_params = [
        ("create_task", Tasks, task_data, "tasks"),
        ("create_label", Labels, {"name": "Created_label"}, "labels"),
        ("create_status", Statuses, {"name": "Created_statuss"}, "statuses")

    ]

    @parameterized.expand(app_create_view_correct_params)
    def test_create_view_form_valid(self, view_name, model, data, revers_view):
        self.assertCreationViewFormValid(view_name, model, data, revers_view)

    app_create_view_incorrect_params = [
        ("create_task", {"name": "new_name"}, "tasks/create_task.html"),
        ("create_label", {"name": ""}, "labels/create_label.html"),
        ("create_status", {"name": ""}, "statuses/create_status.html")
    ]

    @parameterized.expand(app_create_view_incorrect_params)
    def test_create_view_form_invalid(self, view_name, data, template_name):
        self.assertCreationViewFormInValid(view_name, data, template_name)


class UpdateViewsTest(BaseCRUDTest):
    correct_data = {
        "task": {
            "name": "updatetask",
            "description": "updatedescription",
            "status": 1
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
    app_update_view_correct_params = [
        ("update_task", [ITEM_PK], correct_data["task"], "tasks"),
        ("update_label", [ITEM_PK], correct_data["label"], "labels"),
        ("update_status", [ITEM_PK], correct_data["status"], "statuses"),
        ("update_user", [ITEM_PK], correct_data["user"], "users"),
        ('change_password', [ITEM_PK], correct_data["password"], 'users')
    ]

    @parameterized.expand(app_update_view_correct_params)
    def test_update_view_form_valid(self, view_name, pk, data, revers_view):
        self.assertUpdatedViewFormValid(view_name, pk, data, revers_view)

    incorrect_data = {
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

    app_update_view_incorrect_params = [
        (
            "update_task", [ITEM_PK], incorrect_data["task"],
            "tasks/update_task.html"
        ),
        (
            "update_label", [ITEM_PK], incorrect_data["label"],
            "labels/update_label.html"
        ),
        (
            "update_status", [ITEM_PK], incorrect_data["status"],
            "statuses/update_status.html"
        ),
        ("update_user", [ITEM_PK], incorrect_data["user"], "users/update.html"),
        (
            'change_password', [ITEM_PK], incorrect_data["password"],
            'users/change_password.html'
        )
    ]

    @parameterized.expand(app_update_view_incorrect_params)
    def test_update_view_form_invalid(self, view_name, pk, data, template_name):
        self.assertUpdatedViewFormInValid(view_name, pk, data, template_name)


class DeleteViewsTest(BaseCRUDTest):
    app_delete_view_correct_params = [
        ('delete_task', Tasks, 'tasks', ITEM_PK),
        ('delete_label', Labels, 'labels', ITEM_PK),
        ('delete_status', Statuses, 'statuses', ITEM_PK),
    ]

    @parameterized.expand(app_delete_view_correct_params)
    def test_delete_view_form_valid(self, view_name, model, revers_view, pk):
        self.assertDeleteView(view_name, model, revers_view, pk)
