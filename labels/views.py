from .models import Labels
from django.views.generic.list import ListView
from .forms import CreateLabelForm, UpdateLabelForm
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from core.mixins import BaseLoginRequiredMixin
from core.decorators import login_required_message
from django.utils.decorators import method_decorator
from core.base_view_classes import (BaseUpdateView,
                                    BaseDeleteView,
                                    BaseCreateView)
from django.contrib import messages
from django.shortcuts import redirect
# Create your views here.


class LabelsView(BaseLoginRequiredMixin, ListView):
    model = Labels
    template_name = 'labels/index.html'


class CreateLabelView(BaseCreateView):
    form_class = CreateLabelForm
    template_name = 'labels/create_label.html'
    success_url = reverse_lazy('labels')
    success_message = 'Label successfully created'


class UpdateLabelView(BaseUpdateView):
    model = Labels
    form_class = UpdateLabelForm
    template_name = 'labels/update_label.html'
    success_url = reverse_lazy('labels')
    success_message = 'Label has been updated successfully'


class DeleteLabelView(BaseDeleteView):
    model = Labels
    template_name = 'labels/delete_label.html'
    success_url = reverse_lazy('labels')
    success_message = 'Label has been deleted successfully'

    @method_decorator(login_required_message)
    def dispatch(self, request, *args, **kwargs):

        if self.get_object().tasks_set.count() > 0:
            messages.error(request, _("Can't delete label because it's in use"))
            return redirect('labels')
        return super().dispatch(request, *args, **kwargs)
