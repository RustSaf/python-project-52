from django.urls import path

from .views import IndexView, LabelCreateView, LabelDeleteView, LabelUpdateView

app_name = "labels"
urlpatterns = [
    path('',
        IndexView.as_view(),
        name='label_index'
        ),
    path('create/',
        LabelCreateView.as_view(),
        name='label_create',
        ),
    path('<int:pk>/update/',
        LabelUpdateView.as_view(),
        name='label_update',
        ),
    path('<int:pk>/delete/',
        LabelDeleteView.as_view(),
        name='label_delete',
        ),
    ]
