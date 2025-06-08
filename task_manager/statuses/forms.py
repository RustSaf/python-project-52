from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Statuses


class StatusForm(ModelForm):

    def clean(self):

        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        status_exists = name is not None and Statuses.objects.filter(
            name=name).exists()
        
        if status_exists:
            self.fields['name'].widget.attrs.update({
                'class': 'form-control is-invalid'})
            self.add_error(
                'name',
                _("A status with this name already exists.")
                )
        else:
            self.fields['name'].widget.attrs.update({
                'class': 'form-control is-valid'})
        
        return cleaned_data

    class Meta:
        model = Statuses
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


class StatusUpdateForm(StatusForm):

    def clean(self):

        id = self.instance.pk
        name = self.cleaned_data.get('name')
        status_exists = name is not None and Statuses.objects.exclude(
            id=id).filter(name=name).exists()
        
        if status_exists:
            self.fields['name'].widget.attrs.update({
                'class': 'form-control is-invalid'})
            self.add_error(
                'name',
                _("A status with this name already exists.")
                )
        else:
            self.fields['name'].widget.attrs.update({
                'class': 'form-control is-valid'})
        
        return self.cleaned_data