from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import *
from .models import Tasks
from task_manager.users.models import Users
from task_manager.statuses.models import Statuses
from task_manager.labels.models import Labels


class IndexView(View):
    
    def get(self, request, *args, **kwargs):

        statuses = Statuses.objects.all()
        executors = Users.objects.all()
        labels = Labels.objects.all()

        status_id = request.GET.get('status')
        executor_id = request.GET.get('executor')
        label_id = request.GET.get('label')
        is_self_tasks = request.GET.get('self_tasks')

        status = Statuses.objects.get(id=status_id) if status_id else None
        executor = Users.objects.get(id=executor_id) if executor_id else None
        label = Labels.objects.get(id=label_id) if label_id else None
        user = request.user

        tasks_status = Tasks.objects.filter(status=status_id) if status_id else Tasks.objects.all()
        task_executor = Tasks.objects.filter(executor=executor_id) if executor_id else Tasks.objects.all()
        task_label = Tasks.objects.filter(label=label_id) if label_id else Tasks.objects.all()
        self_tasks = Tasks.objects.filter(author=user) if (user and is_self_tasks) else Tasks.objects.all()

        valid = 'is-valid' if (status or executor or label or is_self_tasks) else ''

        tasks = tasks_status & task_executor & task_label & self_tasks


        return render(request, 'tasks/index.html', context={
            'name': _('Tasks'),
            'statuses': statuses,
            'stat': [status_id, status],
            'executors': executors,
            'exec': [executor_id, executor],
            'labels': labels,
            'lab': [label_id, label],
            'valid': valid,
            'checked': is_self_tasks,
            'tasks': tasks,
        })


class TaskCreateView(CreateView):
    
    form_class = TaskForm
    template_name = 'tasks/create.html'

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)  # Получаем данные формы из запроса
        if form.is_valid():  # Проверяем данные формы на корректность
            response = form.save(commit=False)
            response.author = request.user
            response.save()
            messages.success(request, _('Task created successfully'), extra_tags='alert alert-success')
            return redirect('tasks:task_index')
        return render(request, 'tasks/create.html', context={
            'name': _('Create a task'),
            'form': form,
            })


class TaskUpdateView(UpdateView):
    
    model = Tasks
    form_class = TaskForm
    template_name = 'tasks/update.html'

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)  # Получаем данные формы из запроса
        task_id = kwargs.get('pk') 
        task = Tasks.objects.get(id=task_id)
        if form.is_valid():  # Проверяем данные формы на корректность
            response = form.save(commit=False)
            response.id = task_id
            response.author = task.author
            response.created_at = task.created_at
            form.save()
            messages.success(request, _('The task was successfully modified'), extra_tags='alert alert-success')
            return redirect('tasks:task_index')


class TaskDeleteView(DeleteView):
    
    model = Tasks
    success_url = reverse_lazy('tasks:task_index')

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk') 
        task = Tasks.objects.get(id=task_id)
        author = request.user.username
        if task.author == author:
            return render(request, 'tasks/delete.html', context={
                'name': _('Deleting a task'),
                'task': task,
            })
        else:
            messages.error(request, _('A task can only be deleted by its author.'), extra_tags='alert alert-danger')
            return redirect('/tasks')

    def post(self, request, *args, **kwargs):
        messages.success(request, _('Task deleted successfully'), extra_tags='alert alert-success')
        return super().post(request, *args, **kwargs)
