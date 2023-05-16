from task_manager.labels.models import Labels
from django.forms import ModelForm


class CreateLabelForm(ModelForm):
    class Meta:
        model = Labels
        fields = ('name',)


class UpdateLabelForm(CreateLabelForm):
    pass
