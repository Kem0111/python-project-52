from django.forms import ModelForm, ModelChoiceField, Textarea
from django.contrib.auth.models import User
from tasks.models import Tasks
from statuses.models import Statuses
from django.utils.translation import gettext_lazy as _


class CreateTasksForm(ModelForm):

    status = ModelChoiceField(queryset=Statuses.objects.all(),
                              required=True, label=_('status'))
    executor = ModelChoiceField(queryset=User.objects.all(),
                                required=False, label=_('executor'))

    class Meta:
        model = Tasks
        fields = ('name', 'description', 'status', 'executor')
        widgets = {
            'description': Textarea(attrs={'rows': 3}),
        }
        labels = {
            'name': _('Name'),
            'description': _('description'),
        }


class UpdateTaskForm(CreateTasksForm):
    pass
