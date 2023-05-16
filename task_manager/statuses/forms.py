from task_manager.statuses.models import Statuses
from django.forms import ModelForm


class CreateStatusForm(ModelForm):
    class Meta:
        model = Statuses
        fields = ('name',)


class UpdateStatusForm(CreateStatusForm):
    pass
