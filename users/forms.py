from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.utils.translation import gettext_lazy as _


class RegistrationUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'password1', 'password2'
        )


class UpdateUserForm(UserChangeForm):
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password"),
                                required=True)
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password confirmation"),
                                required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        del self.fields['password']

    def clean(self):
        super().clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                self.add_error('password2',
                               _("The entered passwords do not match"))
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get('password1')
        if password1:
            user.set_password(password1)
        if commit:
            user.save()
        return user
