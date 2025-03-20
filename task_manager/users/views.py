from django.shortcuts import get_object_or_404, redirect, render  # type: ignore

from django.utils.translation import gettext_lazy as _
# from django.views.decorators.cache import never_cache
from django.views import View

from task_manager.users.forms import UserForm

# from django.http import Http404
from .models import Users

# class IndexArticleView(View):
#
#     def get(self, request, tags=None, article_id=None):
#         if tags and article_id:
#             return render(request, 'articles/index.html', context={
#                 'tags': tags, 'article_id': article_id
#             })
#         raise Http404()


class IndexView(View):

#     @never_cache
    def get(self, request, *args, **kwargs):
        users = Users.objects.all()[:15]
        return render(request, 'users/index.html', context={
            'name': _('Users'),
            'users': users,
        })


# class LoginView(View):

#     def login_view(request):
#         return render(request, 'login.html', context={'name': _('Input')})

# class ArticleView(View):
#
#    def get(self, request, *args, **kwargs):
#         try:
#        article_id = kwargs.get('id')
#        article = get_object_or_404(Article, id=article_id)
#        comments = ArticleComment.objects.all().order_by('-created_at')[:15]
##        comments = ArticleComment.objects.get('article')
##        print(comments)
##        comments_article = {}
##        for comment in comments: 
##            if comment.article == article:
##                comments_article = {**comments_article, **comment}
##                comment += comment.
##        print(comments_article)
##        comments = ArticleComment.objects.get('article.id').order_by('-created_at')[:15]
##        comments = ArticleComment.objects.select_related('article').order_by('-created_at')[:15]
#        return render(request, 'articles/article.html', context={
#            'article': article,
#            'comments': [comments_article for comments_article in comments if comments_article.article == article],
##            'comments': comments_article,
#        })
##        return render(request, 'articles/article.html', context={
##            'article': article
##        })
##         except Exception:
##             raise Http404()


class UserFormCreateView(View):

    def get(self, request, *args, **kwargs):
        form = UserForm()  # Создаем экземпляр нашей формы
        # Передаем нашу форму в контексте 
        return render(request, 'users/create.html', context={
            'name': _('Registration'), 'form': form
            })  
    
    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)  # Получаем данные формы из запроса
        if form.is_valid():  # Проверяем данные формы на корректность
            form.save()  # Сохраняем форму
            return redirect('user_login')
        return render(request, 'users/create.html', context={
            'name': _('Registration'),
            'form': form
            })


class UserFormEditView(View):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = Users.objects.get(id=user_id)
        form = UserForm(instance=user)
        return render(
            request, 'users/update.html', {'form': form, 'user_id': user_id}
            )
    
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = Users.objects.get(id=user_id)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:index')

        return render(
            request, 'users/update.html', {'form': form, 'user_id': user_id}
            )


class UserFormDeleteView(View):

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = Users.objects.get(id=user_id)
        if user:
            user.delete()
        return redirect('users:index')


# class CommentFormCreateView(View):
# 
#     def get(self, request, *args, **kwargs):
#         form = ArticleCommentForm() # Создаем экземпляр нашей формы
#         article_name = kwargs.get('name')
#         return render(request, 'articles/comment_create.html', context={'form': form, 'name': article_name}) # Передаем нашу форму в контексте
#     
#     def post(self, request, *args, **kwargs):
#         form = ArticleCommentForm(request.POST) # Получаем данные формы из запроса
##        id = form['id']
##        self.cleaned_data['content']
##        art = form['article']        
##        comments = get_object_or_404(ArticleComment, article=art)
##        article_id = comments.article.id
##        article = get_object_or_404(Article, id=article_id)
##        article_id = comments.article.id
##        article = get_object_or_404(Article, article_id)
#         if form.is_valid(): # Проверяем данные формы на корректность
##            article.comment.content = form.cleaned_data['content']
#             form.save() # Сохраняем форму
##            return render(request, 'articles/article.html', context={
##                'article': article,
##                'comments': comments
##            })
#             return redirect('articles:index')
#        return render(request, 'articles/comment_create.html', context={'form': form})
# 
##             comment = form.save(commit=False) # Получаем заполненную модель
#              # Дополнительно обрабатываем модель
##             comment.content = check_for_spam(form.data['content'])
# 
##             comment.save()
