from .models import Labels
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import CreateLabelForm, UpdateLabelForm
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from common.mixins import UserActionMixin, BaseLoginRequiredMixin
from common.decorators import login_required_message
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import redirect
# Create your views here.


class LabelsView(BaseLoginRequiredMixin, ListView):
    model = Labels
    template_name = 'labels/index.html'


class CreateStatusView(UserActionMixin, BaseLoginRequiredMixin, CreateView):
    form_class = CreateLabelForm
    template_name = 'labels/create_label.html'
    success_url = reverse_lazy('labels')

    def form_valid(self, form):
        return super().form_valid(form, _('Label successfully created'))


class UpdateLabelView(UserActionMixin, BaseLoginRequiredMixin, UpdateView):
    model = Labels
    form_class = UpdateLabelForm
    template_name = 'labels/update_label.html'
    success_url = reverse_lazy('labels')

    def form_valid(self, form):
        return super().form_valid(form,
                                  _('Label has been updated successfully'))


class DeleteLabelView(UserActionMixin, BaseLoginRequiredMixin, DeleteView):
    model = Labels
    template_name = 'labels/delete_label.html'
    success_url = reverse_lazy('labels')

    @method_decorator(login_required_message)
    def dispatch(self, request, *args, **kwargs):

        if self.get_object().tasks_set.count() > 0:
            messages.error(request, _("Can't delete label because it's in use"))
            return redirect('labels')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form,
                                  _('Label has been deleted successfully'))
