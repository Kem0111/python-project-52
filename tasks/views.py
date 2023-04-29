from core.mixins import UserActionMixin, BaseLoginRequiredMixin
from django.views.generic import (ListView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  DetailView)
from tasks.models import Tasks
from django.urls import reverse_lazy
from tasks.forms import CreateTasksForm, UpdateTaskForm, TaskFilterForm
from django.utils.translation import gettext as _
from core.decorators import login_required_message
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import redirect


class TasksView(BaseLoginRequiredMixin, ListView):
    model = Tasks
    template_name = 'tasks/index.html'

    def get_queryset(self):
        queryset = queryset = super().get_queryset()
        status_filter = self.request.GET.get('status')
        label_filter = self.request.GET.get('label')
        executor_filter = self.request.GET.get('executor')
        my_tasks_only = self.request.GET.get('my_tasks_only')

        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if label_filter:
            queryset = queryset.filter(labels__pk=label_filter)
        if executor_filter:
            queryset = queryset.filter(executor=executor_filter)
        if my_tasks_only:
            queryset = queryset.filter(author=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TaskFilterForm(self.request.GET or None)
        return context


class CreateTaskView(UserActionMixin, BaseLoginRequiredMixin, CreateView):
    model = Tasks
    form_class = CreateTasksForm
    template_name = 'tasks/create_task.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.author = self.request.user
        task = form.save(commit=False)
        task.save()
        form.save_m2m()
        messages.success(self.request, _('Task successfully created'))
        return redirect(self.success_url)


class UpdateTaskView(BaseLoginRequiredMixin, UpdateView):
    model = Tasks
    form_class = UpdateTaskForm
    template_name = 'tasks/update_task.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        task = form.save(commit=False)
        task.save()
        form.save_m2m()
        messages.success(self.request, _('Task has been updated successfully'))
        return redirect(self.success_url)


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
