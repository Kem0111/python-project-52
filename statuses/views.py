from .models import Statuses
from django.views.generic.list import ListView
from .forms import CreateStatusForm, UpdateStatusForm
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from common.mixins import BaseLoginRequiredMixin
from common.decorators import login_required_message
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import redirect
from tasks.models import Tasks
from common.base_view_classes import (BaseUpdateView,
                                      BaseDeleteView,
                                      BaseCreateView)
# Create your views here.


class StatusesView(BaseLoginRequiredMixin, ListView):
    model = Statuses
    template_name = 'statuses/index.html'


class CreateStatusView(BaseCreateView):
    form_class = CreateStatusForm
    template_name = 'statuses/create_status.html'
    success_url = reverse_lazy('statuses')
    success_message = 'Status successfully created'


class DeleteStatusView(BaseDeleteView):
    model = Statuses
    template_name = 'statuses/delete_status.html'
    success_url = reverse_lazy('statuses')
    success_message = 'Status has been deleted successfully'

    @method_decorator(login_required_message)
    def dispatch(self, request, *args, **kwargs):

        if Tasks.objects.filter(status__id=self.kwargs['pk']):
            messages.error(request, _(
                "Can't delete status because it's in use"
            ))
            return redirect('statuses')
        return super().dispatch(request, *args, **kwargs)


class UpdateStatusView(BaseUpdateView):
    model = Statuses
    form_class = UpdateStatusForm
    template_name = 'statuses/update_status.html'
    success_url = reverse_lazy('statuses')
    success_message = 'Status has been updated successfully'
