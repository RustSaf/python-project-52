from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Statuses


class StatusForm(ModelForm):

    name = forms.CharField(
        required=True,
        label=_("Status"),
        widget=forms.TextInput(attrs={
            'name': "name",
            'maxlength': "150",
            'class': "form-control",
            'placeholder': _("Status"),
            'required': "True",
            'id': "id_name",
            }))

    class Meta:
        model = Statuses
        fields = ['id', 'name']