from django.urls import path

from .views import *


app_name = "tasks"
urlpatterns = [
    path('',
        IndexView.as_view(),
        name='task_index'
    ),
]