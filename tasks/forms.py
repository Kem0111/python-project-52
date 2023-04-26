from django.forms import (ModelForm,
                          ModelChoiceField,
                          Textarea,
                          ModelMultipleChoiceField,
                          CheckboxSelectMultiple)
from django.contrib.auth.models import User
from tasks.models import Tasks
from statuses.models import Statuses
from django.utils.translation import gettext_lazy as _
from labels.models import Labels


class CreateTasksForm(ModelForm):

    status = ModelChoiceField(queryset=Statuses.objects.all(),
                              required=True, label=_('status'))
    executor = ModelChoiceField(queryset=User.objects.all(),
                                required=False, label=_('executor'))
    labels = ModelMultipleChoiceField(
        queryset=Labels.objects.all(),
        widget=CheckboxSelectMultiple,
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


class UpdateTaskForm(CreateTasksForm):
    pass
