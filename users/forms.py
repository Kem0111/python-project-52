from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm


class RegistrationUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'password1', 'password2'
        )


class UpdateUserForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        del self.fields['password']


class CustomPasswordChangeForm(PasswordChangeForm):
    pass
