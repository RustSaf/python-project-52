from django.urls import path

from .views import *

app_name = "tasks"
urlpatterns = [
    path('',
        IndexView.as_view(),
        name='task_index'
        ),
    path('create/',
        TaskCreateView.as_view(),
        name='task_create',
        ),
    path('<int:pk>/update/',
        TaskUpdateView.as_view(),
        name='task_update',
        ),
    path('<int:pk>/delete/',
        TaskDeleteView.as_view(),
        name='task_delete',
        ),
    ]
