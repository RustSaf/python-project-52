from django.urls import path

from .views import *


app_name = "labels"
urlpatterns = [
    path('',
        IndexView.as_view(),
        name='label_index'
    ),
]