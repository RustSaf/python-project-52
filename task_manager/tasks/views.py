from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic import ListView
#from django import forms
#import json
from .forms import *
from .models import Tasks
#from django import forms
#from django.db import models
from task_manager.users.models import Users
from task_manager.statuses.models import Statuses
from task_manager.labels.models import Labels

class IndexView(ListView):

#    
    model = Tasks
    template_name = 'tasks/index.html'
#    success_url = reverse_lazy('tasks:task_index')
#    tasks = Tasks.objects.all()[:]
#    extra_context = {
#        'name': _('Tasks'),
#        'tasks': tasks,
#        }

    def get(self, request, *args, **kwargs):

#        form = TaskForm(request.GET)
#        Tasks.label = models.ForeignKey(Labels, on_delete=models.PROTECT, blank=True, null=True, verbose_name=_("Labels"))
#        form.fields['label'].widget = forms.Select(attrs={
#            'name': "label",
#            'class': "form-select",
#            'placeholder': _("Label"),
#            'id': "id_label",
#            })
       # form.fields['label'] = Labels.objects,
        
        #.attrs.update({
        #        'name': "label",
        #        'class': "form-select",
        #        'placeholder': _("Label"),
        #        'id': "id_label",
        #    })
        statuses = Statuses.objects.all()
        executors = Users.objects.all()
        labels = Labels.objects.all()

        status = request.GET.get('status')
        executor = request.GET.get('executor')
        label = request.GET.get('label')
        author = request.user.id
        self_tasks = Tasks.objects.all().filter(author=author) if author else Tasks.objects.all()
        tasks_status = Tasks.objects.all().filter(status=status) if status else Tasks.objects.all()
        task_executor = Tasks.objects.all().filter(executor=executor) if executor else Tasks.objects.all()
        task_label = Tasks.objects.all().filter(label=label) if label else Tasks.objects.all()

        valid = 'is-valid' if (statuses or executors or labels) else ''

        tasks = tasks_status & task_executor & task_label
        #& self_tasks


        return render(request, 'tasks/index.html', context={
            'name': _('Tasks'),
#            'form': form,
            'statuses': statuses,
            'stat': status,
            'executors': executors,
            'labels': labels,
            'valid': valid,
            'tasks': tasks,
        })


class TaskCreateView(CreateView):
    
#    model = Tasks
#    queryset = Tasks.objects.all()
    form_class = TaskForm
    template_name = 'tasks/create.html'
#    fields = [
#            'id', 'author', 'name', 'discription', 'status', 'executor', 'label'
#    ]
#    fields = ['author']
    success_url = reverse_lazy('tasks:task_index')
    extra_context = {
        'name': _('Create a task'),
        }

#    context_object_name = 'tasks'

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['tasks'] = self.context_object_name

#        return context
#    def get_success_message(self, cleaned_data):
#        return self.success_message % dict(
#            cleaned_data,
#            object=self.object,
#        )

    def post(self, request, *args, **kwargs):
#        super().post(request, *args, **kwargs)
#        creator = Users(request.GET)
        form = TaskForm(request.POST)  # Получаем данные формы из запроса
#        task = Tasks(request.POST)
        author = self.request.user.username
        form.initial = {'author': author}  
        if form.is_valid():  # Проверяем данные формы на корректность
#            task.author = self.request.user.username
            form.clean()
            form.save()
#            task.save()
            messages.success(request, _('Task created successfully'), extra_tags='alert alert-success')
            return redirect('tasks:task_index')
#        messages.success(request, self.request.user.username)

        return render(request, 'tasks/create.html', context={
            'name': _('Create a task'),
            'form': form,
            })

#    def post(self, request, *args, **kwargs):
#        self.author = self.request.username
#        form = TaskForm(request.POST)  # Получаем данные формы из запроса
#        if form.is_valid():  # Проверяем данные формы на корректность    
#            form.clean()
#            instatce = form.save(commit=False)
#            creator = self.request.user.username
#            creator = Users.objects.get(username=author)
#            form.author = 'creator'
#            task = Tasks(request.POST)
#            task.author = creator
#            task.save()
#            instance = form.save(commit=False)
#            instance = form.save()
#            task = Tasks(request.POST)
#            form.author = self.request.user
#            form.author = self.request.user.username
#            form.save()
#            messages.success(request, _('Task created successfully'), extra_tags='alert alert-success')
#            return redirect('tasks:task_index')
#            return super().post(request, *args, **kwargs)
#        return render(request, 'tasks/create.html', context={
#            'name': _('Create a task'),
#            'form': form,
#            })


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
