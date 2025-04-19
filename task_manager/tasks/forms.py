from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Tasks


class TaskForm(ModelForm):

    name = forms.CharField(
        required=True,
        label=_("Task"),
        widget=forms.TextInput(attrs={
            'name': "name",
            'maxlength': "150",
            'class': "form-control",
            'placeholder': _("Task"),
            'required': "True",
            'id': "id_name",
            }))
    discription = forms.CharField(
        required=True,
        label=_("Discription"),
        widget=forms.Textarea(attrs={
            'name': "discription",
            'cols': "40",
            'rows': "10",
            'class': "form-control",
            'placeholder': _("Discription"),
            'id': "id_discription",
            }))
    status = forms.ChoiceField(
        required=True,
        label=_("Status"),
        widget=forms.Select(attrs={
            'name': "status",
            'class': "form-select",
            'placeholder': _("Status"),
            'id': "id_status",
            }))
    executor = forms.ChoiceField(
        required=True,
        label=_("Executor"),
        widget=forms.Select(attrs={
            'name': "executor",
            'class': "form-select",
            'placeholder': _("Executor"),
            'id': "id_executor",
            }))
    label = forms.ChoiceField(
        required=True,
        label=_("Status"),
        widget=forms.SelectMultiple(attrs={
            'name': "label",
            'class': "form-select",
            'placeholder': _("Label"),
            'id': "id_label",
            }))
    

    class Meta:
        model = Tasks
        fields = [
            'id', 'name', 'discription', 'status', 'executor', 'label'
        ]