import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm

# from django.core.exceptions import ValidationError
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
    password1 = forms.CharField(
        required=False,
        label=_("Password"),
        help_text=_("Your password must be at least 3 characters long."),
#        error_messages={'required': _("Required field.")},
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'name': "password1",
#            'required': "False",
#            'required': _("Required field."),
            'autocomplete': "new-password",
            'placeholder': _("Password"),
            'aria-describedby': "id_password1_helptext",
            'id': "id_password1",
        }))
    password2 = forms.CharField(
        required=False,
        label=_("Password confirm"),
        help_text=_("To confirm, please enter the password again."),
#       error_messages={'required': _("Required field.")},
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'name': "password2",
#            'required': "False",
#            'required': _("Required field."),
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
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

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
                _("A user with this name already exists.")
                )
        else:
            self.fields['username'].widget.attrs.update({
                'class': 'form-control is-valid'})
            
#        print(f"Первый пароль: {password1}")
#        if not password1:            
#            raise forms.ValidationError(_("Required field."))
#            self.fields['password1'].widget.attrs.update({
#                'class': 'form-control is-invalid'})
#            self.add_error(
#                'password1',
#                _("Required field.")
#               )
#        elif not password2:
#            raise forms.ValidationError(_("Required field."))
#            self.fields['password2'].widget.attrs.update({
#                'class': 'form-control is-invalid'})
#            self.add_error(
#                'password2',
#                _("Required field.")
#                )
        if password1 != password2:
            self.fields['password2'].widget.attrs.update({
                'class': 'form-control is-invalid'})
            self.add_error(
                'password2',
                _("The passwords entered do not match.")
                )
        elif len(password1) < 3:
            self.fields['password1'].widget.attrs.update({
                'class': 'form-control is-invalid'})
            self.add_error(
                'password1',
                _("""The password you entered is too short.
                    It must support at least 3 characters."""
                    )
                )
        else:
            self.fields['password1'].widget.attrs.update({
                'class': 'form-control is-valid'})       

        return cleaned_data
        
    class Meta:
        
        model = Users
        fields = [
            'id', 'first_name', 'last_name',
            'username', 'password1', 'password2'
            ]
#        error_messages = {
#           'password1': {'required': _("Required field."),},
#            'password2': {'required': _("Required field."),},
#        }


class UserUpdateForm(UserForm):

    def clean(self):

        id = self.instance.pk
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        username = self.cleaned_data.get('username')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
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
                _("A user with this name already exists.")
                )
        else:
            self.fields['username'].widget.attrs.update({
                'class': 'form-control is-valid'})

        if password1 != password2:
            self.fields['password2'].widget.attrs.update({
                'class': 'form-control is-invalid'})
            self.add_error(
                'password2',
                _("The passwords entered do not match.")
                )
        elif len(password1) < 3:
            self.fields['password1'].widget.attrs.update({
                'class': 'form-control is-invalid'})
            self.add_error(
                'password1',
                _("""The password you entered is too short.
                    It must support at least 3 characters."""
                    )
                )
        else:
            self.fields['password1'].widget.attrs.update({
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
            'name': "password1",
            'class': "form-control",
            'placeholder': _("Password"),
            'id': "id_password1",
        }))
    
    class Meta:

        model = Users
        fields = ['username', 'password1']
