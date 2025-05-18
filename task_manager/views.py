from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from .users.forms import LoginUserForm


class IndexView(TemplateView):

    template_name = "index.html"


class LoginUserView(LoginView):

    next = None
    form_class = LoginUserForm
    template_name = 'login.html'
    success_url = reverse_lazy('index')
    extra_context = {'name': _('Entrance'), }

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.success(request, _('You are logged in'), extra_tags='alert alert-success')
            return self.form_valid(form)
        else:
            form.fields['username'].widget.attrs.update({'class': 'form-control is-invalid'})
            form.fields['password'].widget.attrs.update({'class': 'form-control is-invalid'})
            return self.form_invalid(form)


def logout_view(request):
    logout(request)
    messages.success(request, _('You are logged out'), extra_tags='alert alert-primary')
    return redirect('/')
