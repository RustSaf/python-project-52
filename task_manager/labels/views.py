from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from task_manager.tasks.models import Tasks

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
    
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels:label_index')
    extra_context = {
        'name': _('Create a label'),
        }
    
    def post(self, request, *args, **kwargs): 
        messages.success(request, _('Label created successfully'), extra_tags='alert alert-success')
        return super().post(request, *args, **kwargs)


class LabelUpdateView(UpdateView):
    
    model = Labels
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels:label_index')
    extra_context = {'name': _('Change label'), }

    def post(self, request, *args, **kwargs): 
        messages.success(request, _('The label has been changed successfully'), extra_tags='alert alert-success')
        return super().post(request, *args, **kwargs)


class LabelDeleteView(DeleteView):
    
    model = Labels
    success_url = reverse_lazy('labels:label_index')

    def get(self, request, *args, **kwargs):
        label_id = kwargs.get('pk') 
        label = Labels.objects.get(id=label_id)
        return render(request, 'labels/delete.html', context={
            'name': _('Deleting a label'),
            'label': label,
        })      

    def post(self, request, *args, **kwargs):
        label_id = kwargs.get('pk') 
        if Tasks.objects.filter(label=label_id):
            messages.error(request, _('Cannot delete label because it is in use'), extra_tags='alert alert-danger')
            return redirect('/labels')
        else:
            messages.success(request, _('Label successfully removed'), extra_tags='alert alert-success')
            return super().post(request, *args, **kwargs)
