from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .forms import (RegistrationUserForm,
                    UpdateUserForm,)
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from core.mixins import UserActionMixin, UserPermissionMixin
from core.base_view_classes import (BaseUpdateView,
                                    BaseDeleteView)
# Create your views here.


class RegistrationUserView(UserActionMixin, CreateView):
    form_class = RegistrationUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        return super().form_valid(form, _('User successfully registered'))


class UsersView(ListView):
    model = User
    template_name = 'users/index.html'


class UpdateUserView(BaseUpdateView, UserPermissionMixin):
    model = User
    form_class = UpdateUserForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users')
    success_message = 'User information updated successfully'


class DeleteUserView(BaseDeleteView, UserPermissionMixin):
    model = User
    template_name = 'users/delete_user.html'
    success_url = reverse_lazy('users')
    success_message = 'User has been deleted successfully'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.request.user.pk)
