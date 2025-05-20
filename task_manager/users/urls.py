from django.urls import path

from .views import *

app_name = "users"
urlpatterns = [
    path('',
        IndexView.as_view(),
        name='user_index',
        ),
    path('create/',
        UserCreateView.as_view(),
        name='user_create',
        ),
    path('<int:pk>/update/',
        UserUpdateView.as_view(),
        name='user_update',
        ),
    path('<int:pk>/delete/',
        UserDeleteView.as_view(),
        name='user_delete'
        ),
    ]
