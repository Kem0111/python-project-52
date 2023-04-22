from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from typing import Any, Callable
from django.http import HttpRequest


def login_required_message(function: Callable) -> Callable:
    """
    Decorator checks if the user is authenticated. If the user is authenticated,
    they can access the decorated view. Otherwise, they will be redirected
    to the 'login' page with an error message.
    """

    def wrap(request: HttpRequest, *args: Any, **kwargs: Any) -> Any:
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            messages.error(request, _(
                'You are not authorized! Please login'
            ))
            return redirect('login')

    return wrap
