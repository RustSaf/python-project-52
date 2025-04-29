#from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
# from django.views.decorators.cache import never_cache
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, View, ListView
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .users.forms import LoginUserForm
from .users.models import Users


class IndexView(TemplateView):

    template_name = "index.html"
#    def index_view(request):
#        return render(request, 'index.html')


#class IndexAuthView(TemplateView):
#
#    def index_view(request):
#        return render(request, 'base_auth.html')

#LoginRequiredMixin, 
class LoginUserView(LoginView):

    next = None
    form_class = LoginUserForm
    template_name = 'login.html'
    success_url = reverse_lazy('index')
    extra_context = {'name': _('Entrance'),}
#You are not logged in! Please sign in.
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():

#            username = form.cleaned_data['username']
#            password = form.cleaned_data['password']
#            user = authenticate(username=username, password=password)
            messages.success(request, _('You are logged in'), extra_tags='alert alert-success')
            return self.form_valid(form)
        else:
            form.fields['username'].widget.attrs.update({'class': 'form-control is-invalid'})
            form.fields['password'].widget.attrs.update({'class': 'form-control is-invalid'})
#            messages.error(request, 'alert alert-danger')
            return self.form_invalid(form)


def logout_view(request):
    logout(request)
    messages.success(request, _('You are logged out'), extra_tags='alert alert-primary')
    return redirect('/')

#class LogoutUserView(LogoutView):
#
#    next = None
#    form_class = LoginUserForm
#    template_name = 'login.html'
#    success_url = reverse_lazy('index')
#    extra_context = {'name': _('Entrance')}

#class LogoutUserView(LogoutView):
#    pass

#    def post(self, request, *args, **kwargs):
#        form = LoginUserForm(request.POST)
#        form.clean()
#        form.save()  # Сохраняем форму
#        return redirect('login')

#    def get_success_url(self):
#        return reverse_lazy('index')
    
# Вы залогинены (зеленый фон)
# Вы разлогинены (синий фон)

#from django import forms
#
#class loginForm(forms.Form):
#    username = forms.CharField(
#        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your userName'}))
#
#    password = forms.CharField(
#        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'please enter password'}))
#def login_view(request):
#    return render(request, 'login.html', context={'name': _('Input')})



## def article(request):
##     return render(request, 'articles/index.html', context={
##         'article': 'hexlet-django-blog',
##     })
## class IndexArticleView(View):
##
## def get(self, request, *args, **kwargs):
##     return render(request, 'articles/index.html', context={
##         'article': 'hexlet-django-blog',
##     })

## def about(request):
##     return render(request, 'about.html')