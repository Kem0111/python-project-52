from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from .forms import (RegistrationUserForm,
                    UpdateUserForm,
                    CustomPasswordChangeForm)
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import login_required_message
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.contrib.auth.views import PasswordChangeView
# Create your views here.


class RegistrationUserView(CreateView):
    form_class = RegistrationUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        valid = super().form_valid(form)
        messages.success(self.request, _('User successfully registered'))
        return valid


class UsersView(ListView):
    model = User
    template_name = 'users/index.html'


class UpdateUserView(UpdateView, LoginRequiredMixin):
    model = User
    form_class = UpdateUserForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users')

    @method_decorator(login_required_message)
    def dispatch(self, request, *args, **kwargs):
        if request.user.id != int(self.kwargs['pk']):
            messages.error(request, _(
                'You do not have permission to change another user'
            ))
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, _(
            'User information updated successfully'
        ))
        return super().form_valid(form)


class UserPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        messages.success(self.request, _(
            'Password successfully updated'
        ))
        return super().form_valid(form)
