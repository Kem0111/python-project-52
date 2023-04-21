from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _


def login_required_message(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            messages.error(request, _(
                'You are not authorized! Please login'
            ))
            return redirect('login')
    return wrap
