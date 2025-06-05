import re
from urllib import request

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.db.utils import IntegrityError
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Users


class UserForm(ModelForm):

    first_name = forms.CharField(
        required=True,
        label=_("First name"),
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
        label=_("Last name"),
        widget=forms.TextInput(attrs={
            'name': "last_name",
            'maxlength': "150",
            'class': "form-control",
            'placeholder': _("Surname"),
            'id': "id_last_name",
            }))
    username = forms.CharField(
        required=True,
        label=_("Username"),
        help_text=_(
            """Required field. No more than 150 characters.
            Letters, numbers and symbols only @/./+/-/_."""
            ),
        widget=forms.TextInput(attrs={
            'name': "username",
            'maxlength': "150",
            'class': "form-control",
            'placeholder': _("Username"),
            'id': "id_username",
            'autofocus': "True",
            'aria-describedby': "id_username_helptext",
            }))
    password = forms.CharField(
        required=True,
        label=_("Password"),
        help_text=_("Your password must be at least 3 characters long"),
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'name': "password1",
            'autocomplete': "new-password",
            'placeholder': _("Password"),
            'aria-describedby': "id_password1_helptext",
            'id': "id_password1",
        }))
    password_confirm = forms.CharField(
        required=True,
        label=_("Password confirm"),
        help_text=_("To confirm, please enter the password again"),
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'name': "password2",
            'autocomplete': "new-password",
            'placeholder': _("Password confirmation"),
            'aria-describedby': "id_password2_helptext",
            'id': "id_password2",
        }))
    
    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if first_name:
            self.fields['first_name'].widget.attrs.update({
                'class': 'form-control is-valid'})
        
        if last_name:
            self.fields['last_name'].widget.attrs.update({
                'class': 'form-control is-valid'})
        
        pattern = re.compile(r'^[\w@,+-]{1,150}$')
        user_exists = username is not None and Users.objects.filter(
            username=username).exists()

        if not pattern.match(username):
            self.fields['username'].widget.attrs.update({
                'class': 'form-control is-invalid'})
            self.add_error(
                'username',
                _(
                    """Please enter a valid username.
                    It can only contain letters,
                    numbers and @/./+/-/_ signs."""
                    )
                )
        elif user_exists:
            self.fields['username'].widget.attrs.update({
                'class': 'form-control is-invalid'})
            self.add_error(
                'username',
                _("A user with this name already exists")
                )
        else:
            self.fields['username'].widget.attrs.update({
                'class': 'form-control is-valid'})

        if password != password_confirm:
            self.fields['password_confirm'].widget.attrs.update({
                'class': 'form-control is-invalid'})
            self.add_error(
                'password_confirm',
                _("The passwords entered do not match")
                )
        else:
            self.fields['password_confirm'].widget.attrs.update({
                'class': 'form-control is-valid'})
            
        if password:
            if len(password) < 3:
                self.fields['password'].widget.attrs.update({
                    'class': 'form-control is-invalid'})
                self.add_error(
                    'password',
                    _(
                      """The password you entered is too short.
                    It must support at least 3 characters."""
                     )
                    )
            else:
                self.fields['password'].widget.attrs.update({
                    'class': 'form-control is-valid'})

        return cleaned_data
        
    class Meta:
        
        model = Users
        fields = [
            'id', 'first_name', 'last_name',
            'username', 'password', 'password_confirm'
            ]


class UserUpdateForm(UserForm):

    def clean(self):

        id = self.instance.pk
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        
        if first_name:
            self.fields['first_name'].widget.attrs.update({
                'class': 'form-control is-valid'})
        
        if last_name:
            self.fields['last_name'].widget.attrs.update({
                'class': 'form-control is-valid'})
        
        pattern = re.compile(r'^[\w@,+-]{1,150}$')
        user_exists = username is not None and Users.objects.exclude(
            id=id).filter(username=username).exists()

        if not pattern.match(username):
            self.fields['username'].widget.attrs.update({
                'class': 'form-control is-invalid'})
            self.add_error(
                'username',
                _(
                    """Please enter a valid username.
                    It can only contain letters,
                    numbers and @/./+/-/_ signs."""
                    )
                )
        elif user_exists:
            self.fields['username'].widget.attrs.update({
                'class': 'form-control is-invalid'})
            self.add_error(
                'username',
                _("A user with this name already exists")
                )
        else:
            self.fields['username'].widget.attrs.update({
                'class': 'form-control is-valid'})

        if password != password_confirm:
            self.fields['password_confirm'].widget.attrs.update({
                'class': 'form-control is-invalid'})
            self.add_error(
                'password_confirm',
                _("The passwords entered do not match")
                )
        else:
            self.fields['password_confirm'].widget.attrs.update({
                'class': 'form-control is-valid'})

        if len(password) < 3:
            self.fields['password'].widget.attrs.update({
                'class': 'form-control is-invalid'})
            self.add_error(
                'password',
                _(
                    """The password you entered is too short.
                    It must support at least 3 characters."""
                    )
                )
        else:
            self.fields['password'].widget.attrs.update({
                'class': 'form-control is-valid'})

        return self.cleaned_data


class LoginUserForm(AuthenticationForm):

    username = forms.CharField(
        required=True,
        label=_("Username"),
        widget=forms.TextInput(attrs={
            'name': "username",
            'maxlength': "150",
            'class': "form-control",
            'placeholder': _("Username"),
            'id': "id_username",
            'autofocus': "True",
            }))
    password = forms.CharField(
        required=True,
        label=_("Password"),
        widget=forms.PasswordInput(attrs={
            'name': "password",
            'class': "form-control",
            'placeholder': _("Password"),
            'id': "id_password1",
        }))
    
    class Meta:

        model = Users
        fields = ['username', 'password']
