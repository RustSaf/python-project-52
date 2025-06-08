from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView

from .forms import *
from .models import Users


class IndexView(View):

    def get(self, request, *args, **kwargs):
        users = Users.objects.all()
        return render(request, 'users/index.html', context={
            'name': _('Users'),
            'users': users,
        })


class UserCreateView(CreateView):

    model = Users
    form_class = UserForm
    template_name = 'users/create.html'
    extra_context = {'name': _('Registration')}
      
    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)  # Получаем данные формы из запроса
#        if not form.password1 or not form.password2:
#            return render(request, 'users/create.html', context={
#                'name': _('Registration'),
#                'form': form,
#                'empty_pass': _("Required field.")
#                })
        if form.is_valid():  # Проверяем данные формы на корректность
            form.clean()
            form.save()  # Сохраняем форму
            username = form.cleaned_data.get('username', '')
            password = form.cleaned_data.get('password1', '')
            user = Users.objects.get(username=username)
            user.set_password(password)
            user.save()
            messages.success(
                request,
                _('User successfully registered'),
                extra_tags='alert alert-success'
                )
            return redirect('/login')
        return render(request, 'users/create.html', context={
            'name': _('Registration'),
            'form': form
            }) 


class UserUpdateView(LoginRequiredMixin, View):

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
        user_id = kwargs.get('pk')   
        if user_id == self.request.user.id:
            user = Users.objects.get(id=user_id)
            form = UserUpdateForm(instance=user)       
            return render(
                request, 'users/update.html', context={
                    'name': _('Changing user'),
                    'form': form,
                    'user_id': user_id,
                    })        
        else:
            messages.error(
                request,
                _('You do not have permission to modify another user'),
                extra_tags='alert alert-danger'
                )
            return redirect('/users')
  
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = Users.objects.get(id=user_id)
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.clean()
            password = form.cleaned_data.get('password1', '')
            user.set_password(password)
            user.save()
            messages.success(
                request,
                _('User successfully changed'),
                extra_tags='alert alert-success'
                )
            return redirect('/users')

        return render(
            request, 'users/update.html', context={
                'name': _('Changing user'),
                'form': form,
                'user_id': user_id,
                })


class UserDeleteView(LoginRequiredMixin, View):

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
        user_id = kwargs.get('pk') 
        if user_id == self.request.user.id:
            user = Users.objects.get(id=user_id)
            return render(request, 'users/delete.html', context={
                'name': _('Deleting user'),
                'user': user,
            })       
        else:
            messages.error(
                request,
                _('You do not have permission to modify another user'),
                extra_tags='alert alert-danger'
                )
            return redirect('/users')

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = Users.objects.get(id=user_id)
        if user:
            user.delete()
            messages.success(
                request,
                _('User deleted successfully'),
                extra_tags='alert alert-success'
                )
            return redirect('/users')
