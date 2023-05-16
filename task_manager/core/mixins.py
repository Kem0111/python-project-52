from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from typing import Any
from django.http import HttpRequest
from task_manager.core.decorators import login_required_message
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin


class BaseLoginRequiredMixin(LoginRequiredMixin):
    """
    Class BaseLoginRequiredMixin inherits from LoginRequiredMixin and adds
    a custom method decorator to the dispatch method. This decorator shows
    a message to the user when they are required to log in.

    Attributes:
    LoginRequiredMixin: A mixin that requires a user to be authenticated
    to access a view. If not authenticated, they will
    be redirected to the login page.
    Methods:
    dispatch: Takes a request and any arguments for the view, and
    applies the login_required_message decorator before
    calling the parent dispatch method.
    """
    @method_decorator(login_required_message)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserPermissionMixin(LoginRequiredMixin):
    """
    Mixin checks if the user has permission to modify another user.
    If the user does not have permission, they will be redirected
    to the 'users' page with an error message.
    """
    @method_decorator(login_required_message)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Any:
        if request.user.id != int(self.kwargs['pk']):
            messages.error(request, _(
                'You do not have permission to change another user'
            ))
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)


class UserActionMixin:
    """
    Mixin adds a success message to the request when a form is valid.
    The success message is passed as an argument to the form_valid method.
    """

    def form_valid(self, form: Any, success_message: str) -> Any:
        messages.success(self.request, success_message)
        return super().form_valid(form)
