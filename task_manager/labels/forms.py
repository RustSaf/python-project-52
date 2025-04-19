from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Labels


class LabelForm(ModelForm):

    name = forms.CharField(
        required=True,
        label=_("Label"),
        widget=forms.TextInput(attrs={
            'name': "name",
            'maxlength': "150",
            'class': "form-control",
            'placeholder': _("Label"),
            'required': "True",
            'id': "id_name",
            }))

    class Meta:
        model = Labels
        fields = ['id', 'name']