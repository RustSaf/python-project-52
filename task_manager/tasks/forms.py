from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Tasks


class TaskForm(ModelForm):

    class Meta:
        model = Tasks
        fields = [
            'id', 'name', 'author', 'discription',
            'status', 'executor', 'label'
        ]
        required = True
        label = {
            'name': _("Name"),
            'author': _("Author"),
            'discription': _("Discription"),
            'status': _("Status"),
            'executor': _("Executor"),
            'label': _("Label")
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'name': "name",
                'maxlength': "150",
                'class': "form-control",
                'placeholder': _("Name"),
                'required': "True",
                'id': "id_name",
            }),
            'author': forms.HiddenInput(),
            'discription': forms.Textarea(attrs={
                'name': "discription",
                'cols': "40",
                'rows': "10",
                'class': "form-control",
                'placeholder': _("Discription"),
                'id': "id_discription",
            }),
            'status': forms.Select(attrs={
                'name': "status",
                'class': "form-select",
                'placeholder': _("Status"),
                'id': "id_status",
            }),
            'executor': forms.Select(attrs={
                'name': "executor",
                'class': "form-select",
                'placeholder': _("Executor"),
                'id': "id_executor",
            }),
            'label': forms.SelectMultiple(attrs={
                'name': "label",
                'class': "form-select",
                'placeholder': _("Label"),
                'id': "id_label",
            })
        }
