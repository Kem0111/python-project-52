from django.forms import (ModelForm,
                          ModelChoiceField,
                          Textarea,
                          ModelMultipleChoiceField,
                          Form,
                          BooleanField)
from django.contrib.auth.models import User
from tasks.models import Tasks
from statuses.models import Statuses
from django.utils.translation import gettext_lazy as _
from labels.models import Labels


class FullNameUserChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.first_name} {obj.last_name}'


class CreateTasksForm(ModelForm):

    status = ModelChoiceField(queryset=Statuses.objects.all(),
                              required=True, label=_('status'))
    executor = FullNameUserChoiceField(
        queryset=User.objects.all(),
        required=False,
        label=_('executor'),)
    labels = ModelMultipleChoiceField(
        queryset=Labels.objects.all(),
        required=False,
        label=_('Labels')
    )

    class Meta:
        model = Tasks
        fields = ('name', 'description', 'status', 'executor', 'labels')
        widgets = {
            'description': Textarea(attrs={'rows': 3}),
        }
        labels = {
            'name': _('Name'),
            'description': _('description'),
        }


class TaskFilterForm(Form):
    status = ModelChoiceField(
        queryset=Statuses.objects.all(),
        required=False,
        label=_('status')
    )
    executor = ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label=_('executor')
    )
    label = ModelChoiceField(
        queryset=Labels.objects.all(),
        required=False,
        label=_('label')
    )
    my_tasks_only = BooleanField(
        required=False,
        initial=False,
        label=_('My tasks only')
    )


class UpdateTaskForm(CreateTasksForm):
    pass
