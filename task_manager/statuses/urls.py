from django.urls import path

from .views import *


app_name = "statuses"
urlpatterns = [
    path('',
        IndexView.as_view(),
        name='status_index'
    ),
]