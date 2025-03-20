from django.urls import path

# from .views import IndexArticleView
from .views import *  # noqa: F403


app_name = "users"
urlpatterns = [
#    path('<str:tags>/<int:article_id>/',
#        IndexArticleView.as_view(),
#        name='index_'
#    ),
    path('',
        IndexView.as_view(),
        name='user_index'
    ),
    path('<int:pk>/update/',
        UserFormEditView.as_view(),
        name='user_update'
    ),
    path('<int:pk>/delete/',
        UserFormDeleteView.as_view(),
        name='user_delete'),
#    path('<int:id>/',
#         ArticleView.as_view(),
#         name='article_detail'
#    ),
    path('create/',
        UserFormCreateView.as_view(),
        name='user_create'
    ),   
#    path('',
#        LogoutView.as_view(),
#        name='logout'
#    ),
##    path('comment_create/<str:name>',
##         CommentFormCreateView.as_view(),
##         name='comment_create'
##    ),
]

# app_name = "login"
# urlpatterns = [
#     path('',
#         LoginView.as_view(),
#         name='user_login'
#     ),
#]