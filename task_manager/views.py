#from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
# from django.views.decorators.cache import never_cache

# from django.shortcuts import redirect
# from django.urls import reverse
# from django.views import View
from django.views.generic.base import TemplateView


class IndexView(TemplateView):

    def index_view(request):
        return render(request, 'index.html')



#from django import forms
#
#class loginForm(forms.Form):
#    username = forms.CharField(
#        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your userName'}))
#
#    password = forms.CharField(
#        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'please enter password'}))
def login_view(request):
    return render(request, 'login.html', context={'name': _('Input')})



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