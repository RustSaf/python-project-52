from django import forms  # type: ignore # Импортируем формы Django
from django.forms import ModelForm  # type: ignore
from django.utils.translation import gettext_lazy as _

from .models import Users


class UserForm(forms.Form, ModelForm):

    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'name': "first_name",
            'maxlength': "150",
            'class': "form-control",
            'placeholder': _("Name"),
            'required': "True",
            'id': "id_first_name",
            }))
    last_name = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={
            'name': "last_name",
            'maxlength': "150",
            'class': "form-control",
            'placeholder': _("Surname"),
            'id': "id_last_name",
            }))
    username = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={
            'name': "username",
            'maxlength': "150",
            'class': "form-control",
            'placeholder': _("Username"),
            'id': "id_username",
            'autofocus': "True",
            'aria-describedby': "id_username_helptext",
            }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control",
        'name': "password1",
        'autocomplete': "new-password",
        'placeholder': _("Password"),
        'aria-describedby': "id_password1_helptext",
        'id': "id_password1",
        }))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control",
        'name': "password2",
        'autocomplete': "new-password",
        'placeholder': _("Password confirmation"),
        'aria-describedby': "id_password2_helptext",
        'id': "id_password2",
        }))

    class Meta:
        model = Users
        fields = [
            'first_name', 'last_name', 'username', 'password', 'password_confirm'
            ]
