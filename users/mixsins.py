from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from typing import Any
from django.http import HttpRequest


class UserPermissionMixin:
    """
    Mixin checks if the user has permission to modify another user.
    If the user does not have permission, they will be redirected
    to the 'users' page with an error message.
    """

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
