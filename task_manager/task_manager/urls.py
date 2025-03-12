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
    path('users/', views.users_view, name='users'),
    path('users/create/', views.users_create_view, name='users/create'),
    path('login/', views.login_view, name='login'),
#   path('about/', views.about, name='about'),
#   path('articles/',
#       include('hexlet_django_blog.article.urls', namespace='articles_'),
#   ),
    path("admin/", admin.site.urls),
]

