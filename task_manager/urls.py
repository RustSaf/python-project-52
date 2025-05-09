"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin  # noqa: I001
# from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.urls import reverse, reverse_lazy
# from task_manager.users.forms import UserForm

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
#    path('auth/', views.IndexAuthView.index_view, name='index_auth'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'), 
#    path('logout/', LogoutView.as_view(http_method_names=['post'],
#        next_page = reverse_lazy('index')),
#        template_name='logout.html',
#        next_page=None),
#        name='logout'),
#    (r'^accounts/', include('registration.backends.default.urls')),
    path('users/',
        include('task_manager.users.urls', namespace='users'),
        ),
    path('statuses/',
        include('task_manager.statuses.urls', namespace='statuses'),
        ),   
    path('labels/',
        include('task_manager.labels.urls', namespace='labels'),
        ),
    path('tasks/',
        include('task_manager.tasks.urls', namespace='tasks'),
        ),
    path("admin/", admin.site.urls),
]