from task_manager.core.mixins import UserActionMixin, BaseLoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.translation import gettext as _


class BaseActionView(UserActionMixin, BaseLoginRequiredMixin):

    def form_valid(self, form):
        return super().form_valid(form, _(self.success_message))


class BaseUpdateView(BaseActionView, UpdateView):
    pass


class BaseDeleteView(BaseActionView, DeleteView):
    pass


class BaseCreateView(BaseActionView, CreateView):
    pass
