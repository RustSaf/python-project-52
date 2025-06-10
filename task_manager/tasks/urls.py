from django.urls import path

from .views import (
    IndexView,
    TaskCreateView,
    TaskDeleteView,
    TaskInfoView,
    TaskUpdateView,
)

app_name = "tasks"
urlpatterns = [
    path('',
        IndexView.as_view(),
        name='task_index'
        ),
    path('<int:pk>/',
        TaskInfoView.as_view(),
        name='task_info',
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
