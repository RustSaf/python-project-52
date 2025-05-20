from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Labels


class LabelForm(ModelForm):

    class Meta:
        model = Labels
        fields = ['name']
        required = True
        label = {
            'name': _("Name"),
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'name': "name",
                'maxlength': "150",
                'class': "form-control",
                'placeholder': _("Name"),
                'required': "True",
                'id': "id_name",
        })}
