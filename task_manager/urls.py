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
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.IndexView.index_view, name='index'),
    path('login/', views.login_view, name='user_login'),
#    path('login/',
#        include('task_manager.users.urls', namespace='login_'),
#    ),
    path('users/',
        include('task_manager.users.urls', namespace='users_'),
    ),
#    path('login/',
#        include('task_manager.users.urls', namespace='login'),
#    ),
#    path('logout/',
#        include('task_manager.users.urls', namespace='logout'),
#    ),
    path("admin/", admin.site.urls),
]
