from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .forms import (RegistrationUserForm,
                    UpdateUserForm,
                    CustomPasswordChangeForm)
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.contrib.auth.views import PasswordChangeView
from common.mixins import UserActionMixin, UserPermissionMixin
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


class UpdateUserView(UserActionMixin, UserPermissionMixin,
                     UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        return super().form_valid(
            form, _('User information updated successfully')
        )


class UserPasswordChangeView(UserActionMixin, UserPermissionMixin,
                             PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        return super().form_valid(form, _('Password successfully updated'))


class DeleteUserView(UserActionMixin, UserPermissionMixin,
                     DeleteView):
    model = User
    template_name = 'users/delete_user.html'
    success_url = reverse_lazy('index')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pk=self.request.user.pk)

    def form_valid(self, form):
        return super().form_valid(form, _('User has been deleted successfully'))
