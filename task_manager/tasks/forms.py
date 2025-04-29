from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Tasks
from task_manager.users.models import Users
#from task_manager.statuses.models import Statuses
#from task_manager.labels.models import Labels


class TaskForm(ModelForm):

#    author = forms.CharField(
#        label=_("Author"),
#        widget=forms.HiddenInput())

#    def clean(self):
#        cleaned_data = super().clean()
#        name = self.cleaned_data.get('name')
#        author = self.cleaned_data.get('author')  
#        discription = self.cleaned_data.get('discription')
#        status = self.cleaned_data.get('status')
#        executor = self.cleaned_data.get('executor')
#        label = self.cleaned_data.get('label')

#        return cleaned_data


#    def post(self, request, *args, **kwargs):
#        super().post(request, *args, **kwargs)
#        author = Users(request.GET)
##        creator = self.request.user.username
#        self.fields['author'].initial = author.username

#    author = forms.HiddenInput()

#    author = forms.CharField(
#        required=True,
#        label=_("Author"),
#        widget=forms.HiddenInput()
#    )
#    name = forms.CharField(
#        required=True,
#        label=_("Task"),
#        widget=forms.TextInput(attrs={
#            'name': "name",
#            'maxlength': "150",
#            'class': "form-control",
#            'placeholder': _("Task"),
#            'required': "True",
#            'id': "id_name",
#            }))
#    discription = forms.CharField(
#        required=True,
#        label=_("Discription"),
#        widget=forms.Textarea(attrs={
#            'name': "discription",
#            'cols': "40",
#            'rows': "10",
#            'class': "form-control",
#            'placeholder': _("Discription"),
#            'id': "id_discription",
#            }))
#    status = forms.ModelChoiceField(
#        required=True,
#        label=_("Status"),
#        choices=Statuses.objects,
#        queryset=Statuses.objects,
#        choices=Tasks.status,
#        widget=forms.Select(attrs={
#            'name': "status",
#            'class': "form-select",
#            'placeholder': _("Status"),
#            'id': "id_status",
#            }))
#    executor = forms.ModelChoiceField(
#        required=True,
#        label=_("Executor"),
#        queryset=Users.objects,
#        widget=forms.Select(attrs={
#            'name': "executor",
#            'class': "form-select",
#            'placeholder': _("Executor"),
#            'id': "id_executor",
#            }))
#    label = forms.ModelMultipleChoiceField(
#        required=True,
#        label=_("Label"),
#        queryset=Labels.objects,
#        widget=forms.SelectMultiple(attrs={
#            'name': "label",
#            'class': "form-select",
#            'placeholder': _("Label"),
#            'id': "id_label",
#            }))

    class Meta:
        model = Tasks
        fields = [
            'name', 'author', 'discription', 'status', 'executor', 'label'
        ]
        required=True
        label = {
            'author': _("Author"),
            'name': _("Name"),
            'discription': _("Discription"),
            'status': _("Status"),
            'executor': _("Executor"),
            'label': _("Label")
        }
        widgets = {
            'author': forms.HiddenInput(),
            'name': forms.TextInput(attrs={
                'name': "name",
                'maxlength': "150",
                'class': "form-control",
                'placeholder': _("Name"),
                'required': "True",
                'id': "id_name",
            }),
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
