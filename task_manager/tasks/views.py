from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView

from .forms import *
from .models import Tasks



class IndexView(View):

#    
#    model = Tasks
#    template_name = 'users/index.html'
#    success_url = reverse_lazy('')
#    tasks = Tasks.objects.all()[:]
#    extra_context = {
#        'name': _('Tasks'),
#        'tasks': tasks,
#        }
    def get(self, request, *args, **kwargs):
        tasks = Tasks.objects.all()[:]
        return render(request, 'tasks/index.html', context={
            'name': _('Tasks'),
            'tasks': tasks,
        })


class TaskCreateView(CreateView):
    
    model = Tasks
    form_class = TaskForm
    template_name = 'tasks/create.html'
#    fields = [
#            'id', 'name', 'discription', 'status', 'executor', 'label'
#        ]
    success_url = reverse_lazy('tasks:task_index')
    extra_context = {
        'name': _('Create a task'),
        }
    
    def post(self, request, *args, **kwargs): 
        messages.success(request, _('Task created successfully'), extra_tags='alert alert-success')
        return super().post(request, *args, **kwargs)


# form_class = UserForm
#   template_name = 'users/create.html'
#    success_url = reverse_lazy('login')
#    extra_context = {'name': _('Registration'),}
class TaskUpdateView(UpdateView):
    
    model = Tasks
    form_class = TaskForm
    template_name = 'tasks/update.html'
#    fields = [
#            'id', 'name', 'discription', 'status', 'executor', 'label'
#        ]
    success_url = reverse_lazy('tasks:task_index')
    extra_context = {'name': _('Changing a task'),}

    def post(self, request, *args, **kwargs): 
        messages.success(request, _('The task was successfully modified'), extra_tags='alert alert-success')
        return super().post(request, *args, **kwargs)


class TaskDeleteView(DeleteView):
    
    model = Tasks
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:task_index')

    def post(self, request, *args, **kwargs):
        messages.success(request, _('Task deleted successfully'), extra_tags='alert alert-success')
        return super().post(request, *args, **kwargs)

#    def get(self, request, *args, **kwargs):
#        task_id = kwargs.get('id')
#        user_id = self.request.user.id
#        task = Tasks.objects.get(id=task_id)
#        author = Users.objects.get(id=user_id)
#        if task['author'] == author:
#            return render(request, 'tasks/delete.html', context={
#                'name': _('Deleting a task'),
#                'task': task['name'],
#            })        
#        else:
#            messages.error(request, _('A task can only be deleted by its author.'), extra_tags='alert alert-danger')
#            return redirect('/tasks')

#    def post(self, request, *args, **kwargs):
#        task_id = kwargs.get('pk')
#        task = Tasks.objects.get(id=task_id)
#        if task:
#            task.delete()
#            messages.success(request, _('Task deleted successfully'), extra_tags='alert alert-success')            
#            return redirect('/tasks')


# Фильтр
#
# select Статус
# select Исполнитель
# select Метка
# checkbox Только свои задачи
# кнопка Показать

# ID 	Имя 	Статус 	Автор 	Исполнитель 	Дата создания


# Create a task
# Task created successfully

# Changing a task
# The task was successfully modified

# Deleting a task
# A task can only be deleted by its author.
# Are you sure you want to delete {}? (все как при удалении пользователя)
# Task deleted successfully
