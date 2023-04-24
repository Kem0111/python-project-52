from .models import Statuses
from django.forms import ModelForm


class CreateStatusForm(ModelForm):
    class Meta:
        model = Statuses
        fields = ('name',)


class UpdateStatusForm(CreateStatusForm):
    pass
