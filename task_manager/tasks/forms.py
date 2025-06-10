from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Tasks


class TaskForm(ModelForm):

    def clean(self):

        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        task_exists = name is not None and Tasks.objects.filter(
            name=name).exists()
        
        if task_exists:
            self.fields['name'].widget.attrs.update({
                'class': 'form-control is-invalid'})
            self.add_error(
                'name',
                _("A task with this name already exists.")
                )
        else:
            self.fields['name'].widget.attrs.update({
                'class': 'form-control is-valid'})
        
        return cleaned_data

    class Meta:
        model = Tasks
        fields = [
            'id', 'name', 'author', 'discription',
            'status', 'executor', 'labels'
        ]
        required = True
        label = {
            'name': _("Name"),
            'author': _("Author"),
            'discription': _("Discription"),
            'status': _("Status"),
            'executor': _("Executor"),
            'label': _("Labels")
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'maxlength': "150",
                'class': "form-control",
                'placeholder': _("Name"),
                'required': "True",
                'id': "id_name",
            }),
            'author': forms.HiddenInput(),
            'discription': forms.Textarea(attrs={
                'cols': "40",
                'rows': "10",
                'class': "form-control",
                'placeholder': _("Discription"),
                'id': "id_description",
            }),
            'status': forms.Select(attrs={
                'required': "True",
                'class': "form-select",
                'id': "id_status",
            }),
            'executor': forms.Select(attrs={
                'class': "form-select",
                'id': "id_executor",
            }),
            'labels': forms.SelectMultiple(attrs={
                'class': "form-select",
                'id': "id_labels",
            })
        }


class TaskUpdateForm(TaskForm):

    def clean(self):

        id = self.instance.pk
        name = self.cleaned_data.get('name')
        task_exists = name is not None and Tasks.objects.exclude(
            id=id).filter(name=name).exists()
        
        if task_exists:
            self.fields['name'].widget.attrs.update({
                'class': 'form-control is-invalid'})
            self.add_error(
                'name',
                _("A task with this name already exists.")
                )
        else:
            self.fields['name'].widget.attrs.update({
                'class': 'form-control is-valid'})
        
        return self.cleaned_data
