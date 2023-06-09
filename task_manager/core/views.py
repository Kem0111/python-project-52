from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from task_manager.core.forms import LoginUserForm
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.utils.translation import gettext as _


class HomePageView(TemplateView):

    template_name = 'index.html'

    def get(self, request, **kwargs):
        return render(request, 'index.html')


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def form_valid(self, form):
        messages.success(self.request, _('You are successfully logged in'))
        return super().form_valid(form)


class LogoutUserView(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You have successfully logged out'))
        return super().dispatch(request, *args, **kwargs)


def handling_404(request, exeption):
    return render(request, '404.html', status=404)
