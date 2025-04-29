from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView

from .forms import *
from .models import Statuses



class IndexView(View):

    def get(self, request, *args, **kwargs):
        statuses = Statuses.objects.all()
        return render(request, 'statuses/index.html', context={
            'name': _('Statuses'),
            'statuses': statuses,
        })


class StatusCreateView(CreateView):
    
#    model = Statuses
    form_class = StatusForm
    template_name = 'statuses/create.html'
#    fields = [
#            'id', 'name', 'discription', 'status', 'executor', 'label'
#        ]
    success_url = reverse_lazy('statuses:status_index')
    extra_context = {
        'name': _('Create status'),
        }
    
    def post(self, request, *args, **kwargs): 
        messages.success(request, _('Status created successfully'), extra_tags='alert alert-success')
        return super().post(request, *args, **kwargs)


# form_class = UserForm
#   template_name = 'users/create.html'
#    success_url = reverse_lazy('login')
#    extra_context = {'name': _('Registration'),}
class StatusUpdateView(UpdateView):
    
    model = Statuses
    form_class = StatusForm
    template_name = 'statuses/update.html'
#    fields = [
#            'id', 'name', 'discription', 'status', 'executor', 'label'
#        ]
    success_url = reverse_lazy('statuses:status_index')
    extra_context = {'name': _('Change of status'),}

    def post(self, request, *args, **kwargs): 
        messages.success(request, _('Status changed successfully'), extra_tags='alert alert-success')
        return super().post(request, *args, **kwargs)


class StatusDeleteView(DeleteView):
    
    model = Statuses
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses:status_index')

    def post(self, request, *args, **kwargs):
        messages.success(request, _('Status deleted successfully'), extra_tags='alert alert-success')
        return super().post(request, *args, **kwargs)
# ID 	Имя 	Дата создания

# Create status
# Status created successfully

# Change of status
# Status changed successfully

# Deleting status
# Are you sure you want to delete {}? (все как при удалении пользователя)
# Cannot delete status because it is in use
# Status deleted successfully
