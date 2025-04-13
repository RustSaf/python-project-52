from django.urls import path

from .views import *


app_name = "users"
urlpatterns = [
#    path('<str:tags>/<int:article_id>/',
#        IndexArticleView.as_view(),
#        name='index_'
#    ),
    path('',
        IndexView.as_view(),
        name='user_index',
    ),
#    path('auth/',
#        IndexAuthView.as_view(),
#        name='user_index_auth',
#    ),
    path('<int:pk>/update/',
        UserEditView.as_view(),
        name='user_update',
    ),
    path('<int:pk>/delete/',
        UserDeleteView.as_view(),
        name='user_delete'),
#    path('<int:id>/',
#         ArticleView.as_view(),
#         name='article_detail'
#    ),
    path('create/',
        UserCreateView.as_view(),
        name='user_create',
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