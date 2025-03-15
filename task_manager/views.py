#from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
##from django.views import View
from django.views.generic.base import TemplateView
from django.views.decorators.cache import never_cache


##def index(request):
##    return render(request, 'index.html', context={
##        'who': 'World',
##    })
class IndexView(TemplateView):
##
    template_name = "index.html"
##
##    def get_context_data(self):
##       context = super().get_context_data(**kwargs)
##        context['who'] = 'World'
##        return context
    @never_cache
    def index_view(request):
##    return redirect(reverse('article', kwargs={'tags': 'python', 'article_id': 42}))
##        return redirect(reverse('article:index', kwargs={'tags': 'python', 'article_id': 42}))
        return render(request, 'index.html')
#       , context={'who': 'World',})

@never_cache
def users_view(request):
    return render(request, 'users.html', context={'name': 'Users'})

@never_cache
def login_view(request):
    return render(request, 'login.html', context={'name': 'Input'})

@never_cache
def users_create_view(request):
    return render(request, 'create.html', context={'name': 'Registration'})
##def article(request):
##    return render(request, 'articles/index.html', context={
##        'article': 'hexlet-django-blog',
##    })
##class IndexArticleView(View):
##
##    def get(self, request, *args, **kwargs):
##        return render(request, 'articles/index.html', context={
##            'article': 'hexlet-django-blog',
##        })

# def about(request):
#    return render(request, 'about.html')