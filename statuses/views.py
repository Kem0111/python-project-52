from .models import Statuses
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import CreateStatusForm, UpdateStatusForm
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from common.mixins import UserActionMixin, BaseLoginRequiredMixin
from common.decorators import login_required_message
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import redirect
from tasks.models import Tasks
# Create your views here.


class StatusesView(BaseLoginRequiredMixin, ListView):
    model = Statuses
    template_name = 'statuses/index.html'


class CreateStatusView(UserActionMixin, BaseLoginRequiredMixin, CreateView):
    form_class = CreateStatusForm
    template_name = 'statuses/create_status.html'
    success_url = reverse_lazy('statuses')

    def form_valid(self, form):
        return super().form_valid(form, _('Status successfully created'))


class DeleteStatusView(UserActionMixin, BaseLoginRequiredMixin, DeleteView):
    model = Statuses
    template_name = 'statuses/delete_status.html'
    success_url = reverse_lazy('statuses')

    @method_decorator(login_required_message)
    def dispatch(self, request, *args, **kwargs):

        if Tasks.objects.filter(status__id=self.kwargs['pk']):
            messages.error(request, _(
                "Can't delete status because it's in use"
            ))
            return redirect('statuses')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form,
                                  _('Status has been deleted successfully'))


class UpdateStatusView(UserActionMixin, BaseLoginRequiredMixin, UpdateView):
    model = Statuses
    form_class = UpdateStatusForm
    template_name = 'statuses/update_status.html'
    success_url = reverse_lazy('statuses')

    def form_valid(self, form):
        return super().form_valid(form,
                                  _('Status has been updated successfully'))
