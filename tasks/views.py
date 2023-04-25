from common.mixins import UserActionMixin, BaseLoginRequiredMixin
from django.views.generic import (ListView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  DetailView)
from tasks.models import Tasks
from django.urls import reverse_lazy
from tasks.forms import CreateTasksForm, UpdateTaskForm
from django.utils.translation import gettext as _
from common.decorators import login_required_message
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import redirect


class TasksView(BaseLoginRequiredMixin, ListView):
    model = Tasks
    template_name = 'tasks/index.html'


class CreateTaskView(UserActionMixin, BaseLoginRequiredMixin, CreateView):
    model = Tasks
    form_class = CreateTasksForm
    template_name = 'tasks/create_task.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form, _('Task successfully created'))


class UpdateTaskView(UserActionMixin, BaseLoginRequiredMixin, UpdateView):
    model = Tasks
    form_class = UpdateTaskForm
    template_name = 'tasks/update_task.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        return super().form_valid(form,
                                  _('Task has been updated successfully'))


class DeleteTaskView(UserActionMixin, BaseLoginRequiredMixin, DeleteView):
    model = Tasks
    template_name = 'tasks/delete_task.html'
    success_url = reverse_lazy('tasks')

    @method_decorator(login_required_message)
    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.author != request.user:
            messages.error(request, _(
                "A task can only be deleted by its author"
            ))
            return redirect('tasks')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form,
                                  _('Task has been deleted successfully'))


class TaskView(BaseLoginRequiredMixin, DetailView):
    model = Tasks
    template_name = 'tasks/task_view.html'
