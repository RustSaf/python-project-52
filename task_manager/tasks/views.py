from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from task_manager.labels.models import Labels
from task_manager.statuses.models import Statuses
from task_manager.users.models import Users

from .forms import *
from .models import Tasks


class IndexView(LoginRequiredMixin, View):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request,
                _('You are not logged in! Please sign in.'),
                extra_tags='alert alert-danger'
                )
            return self.handle_no_permission()
        return super(
            LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

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

        tasks_status = Tasks.objects.filter(
            status=status_id) if status_id else Tasks.objects.all()
        task_executor = Tasks.objects.filter(
            executor=executor_id) if executor_id else Tasks.objects.all()
        task_label = Tasks.objects.filter(
            label=label_id) if label_id else Tasks.objects.all()
        self_tasks = Tasks.objects.filter(
            author=user) if (user and is_self_tasks) else Tasks.objects.all()

        valid = 'is-valid' if (
            status or executor or label or is_self_tasks) else ''

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


class TaskCreateView(LoginRequiredMixin, CreateView):
    
    model = Tasks
    form_class = TaskForm
    template_name = 'tasks/create.html'
    extra_context = {'name': _('Create a task')}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request,
                _('You are not logged in! Please sign in.'),
                extra_tags='alert alert-danger'
                )
            return self.handle_no_permission()
        return super(
            LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)  # Получаем данные формы из запроса
        if form.is_valid():  # Проверяем данные формы на корректность
            form.clean()
            response = form.save(commit=False)
            response.author = request.user
            response.save()
            messages.success(
                request,
                _('Task created successfully'),
                extra_tags='alert alert-success'
                )
            return redirect('tasks:task_index')
        return render(request, 'tasks/create.html', context={
            'form': form,
            })


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    
    model = Tasks
    form_class = TaskUpdateForm
    template_name = 'tasks/update.html'
    extra_context = {'name': _('Changing a task')}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request,
                _('You are not logged in! Please sign in.'),
                extra_tags='alert alert-danger'
                )
            return self.handle_no_permission()
        return super(
            LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = TaskUpdateForm(request.POST)  # Получаем данные формы из запроса
        task_id = kwargs.get('pk') 
        task = Tasks.objects.get(id=task_id)
        author = task.author
        form = TaskUpdateForm(request.POST, instance=task)
        if form.is_valid():  # Проверяем данные формы на корректность
            form.clean()
            form.save()
            task.author = author
            task.save()
            messages.success(
                request,
                _('The task was successfully modified'),
                extra_tags='alert alert-success'
                )
            return redirect('tasks:task_index')
        return render(request, 'tasks/update.html', context={
                'form': form,
                'task_id': task_id,
                })


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    
    model = Tasks
    success_url = reverse_lazy('tasks:task_index')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request,
                _('You are not logged in! Please sign in.'),
                extra_tags='alert alert-danger'
                )
            return self.handle_no_permission()
        return super(
            LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

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
            messages.error(
                request,
                _('A task can only be deleted by its author'),
                extra_tags='alert alert-danger'
                )
            return redirect('/tasks')

    def post(self, request, *args, **kwargs):
        messages.success(
            request,
            _('Task deleted successfully'),
            extra_tags='alert alert-success'
            )
        return super().post(request, *args, **kwargs)
