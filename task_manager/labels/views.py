from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView

from .forms import *
from .models import Labels



class IndexView(View):

    def get(self, request, *args, **kwargs):
        labels = Labels.objects.all()
        return render(request, 'labels/index.html', context={
            'name': _('Labels'),
            'labels': labels,
        })
    

class LabelCreateView(CreateView):
    
    model = Labels
    form_class = LabelForm
    template_name = 'labels/create.html'
#    fields = [
#            'id', 'name', 'discription', 'status', 'executor', 'label'
#        ]
    success_url = reverse_lazy('labels:label_index')
    extra_context = {
        'name': _('Create a label'),
        }
    
    def post(self, request, *args, **kwargs): 
        messages.success(request, _('Label created successfully'), extra_tags='alert alert-success')
        return super().post(request, *args, **kwargs)


# form_class = UserForm
#   template_name = 'users/create.html'
#    success_url = reverse_lazy('login')
#    extra_context = {'name': _('Registration'),}
class LabelUpdateView(UpdateView):
    
    model = Labels
    form_class = LabelForm
    template_name = 'labels/update.html'
#    fields = [
#            'id', 'name', 'discription', 'status', 'executor', 'label'
#        ]
    success_url = reverse_lazy('labels:label_index')
    extra_context = {'name': _('Change label'),}

    def post(self, request, *args, **kwargs): 
        messages.success(request, _('The label has been changed successfully'), extra_tags='alert alert-success')
        return super().post(request, *args, **kwargs)


class LabelDeleteView(DeleteView):
    
#    model = Labels
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels:label_index')

    def post(self, request, *args, **kwargs):
        messages.success(request, _('Label successfully removed'), extra_tags='alert alert-success')
        return super().post(request, *args, **kwargs)
# ID 	Имя 	Дата создания

# Create a label
# Label created successfully

# Change label
# The label has been changed successfully.

# Deleting a label
# Are you sure you want to delete {}? (все как при удалении пользователя)
# Cannot delete label because it is in use
# Label successfully removed