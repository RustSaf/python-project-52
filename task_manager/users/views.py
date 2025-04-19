from django.shortcuts import get_object_or_404, redirect, render  # type: ignore
from django.urls import reverse, reverse_lazy

from django.utils.translation import gettext_lazy as _
# from django.views.decorators.cache import never_cache
from django.views import View
from django import forms
from django.contrib import messages
# from django.contrib.messages import get_messages
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
#from django.contrib.auth.hashers import make_password

from .forms import *

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

    def get(self, request, *args, **kwargs):
        users = Users.objects.all()[:]
        return render(request, 'users/index.html', context={
            'name': _('Users'),
            'users': users,
        })


#class IndexAuthView(View):
#
#    def get(self, request, *args, **kwargs):
#        users = Users.objects.all()[:]
#        return render(request, 'users/index_auth.html', context={
#            'name': _('Users'),
#            'users': users,
#        })

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


#LoginRequiredMixin
class UserCreateView(View):
#    form_class = UserForm
#   template_name = 'users/create.html'
#    success_url = reverse_lazy('login')
#    extra_context = {'name': _('Registration'),}
    
#    def post(self, request, *args, **kwargs):
#        self.object = None
#        messages.success(request, _('User successfully registered'), extra_tags='alert alert-success')
#        return super().post(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = UserForm()  # Создаем экземпляр нашей формы
        # Передаем нашу форму в контексте 
        return render(request, 'users/create.html', context={
            'name': _('Registration'),
            'form': form,
            })
      
    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)  # Получаем данные формы из запроса
        if form.is_valid():  # Проверяем данные формы на корректность
            form.clean()
#            form.set_password(form.password)
#            form.make_password(form.password)
            form.save()  # Сохраняем форму
            messages.success(request, _('User successfully registered'), extra_tags='alert alert-success')
            return redirect('/login')
        return render(request, 'users/create.html', context={
            'name': _('Registration'),
            'form': form,
            })
 
# 
#       
#        messages.error(request, _("A user with this name already exists."))
# The passwords entered do not match.
# Введённый пароль слишком короткий. Он должен содержать как минимум 3 символа.
#        if form.errors:
#            messages.error(request, _("Please enter a valid username. It can only contain letters, numbers and @/./+/-/_ signs."), extra_tags="username")
#        if form.password.errors:
#            messages.error(request, _("The password you entered is too short. It must contain at least 3 characters."), extra_tags="password_length")
#        if form.passsword != form.password_confirm:
#            messages.error(request, _("The passwords entered do not match."), extra_tags="password_alert")
#        form.widget.attrs.update({'class':'form-control is-invalid'})


class UserUpdateView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _('You are not logged in! Please sign in.'), extra_tags='alert alert-danger')
            return self.handle_no_permission()
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')   
        if user_id == self.request.user.id:
            user = Users.objects.get(id=user_id)
            form = UserUpdateForm(instance=user)       
            return render(
                request, 'users/update.html', context={
                    'name': _('Change user'),
                    'form': form,
                    'user_id': user_id,
                    })
# У вас нет прав для изменения другого пользователя.(красное)         
        else:
            messages.error(request, _('You do not have permission to modify another user.'), extra_tags='alert alert-danger')
            return redirect('/users')
  
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = Users.objects.get(id=user_id)
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.clean()
            form.save()
            messages.success(request, _('User successfully changed'), extra_tags='alert alert-success')
            return redirect('/users')

        return render(
            request, 'users/update.html', {
                'name': _('Change user'),
                'form': form,
                'user_id': user_id,
                })


class UserDeleteView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _('You are not logged in! Please sign in.'), extra_tags='alert alert-danger')
            return self.handle_no_permission()
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
# У вас нет прав для изменения другого пользователя.(красное)
        user_id = kwargs.get('pk') 
        if user_id == self.request.user.id:
            user = Users.objects.get(id=user_id)
            return render(request, 'users/delete.html', context={
                'name': _('Delete user'),
                'user': user,
            })
        # У вас нет прав для изменения другого пользователя.(красное)         
        else:
            messages.error(request, _('You do not have permission to modify another user.'), extra_tags='alert alert-danger')
            return redirect('/users')

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = Users.objects.get(id=user_id)
        if user:
            user.delete()
            messages.success(request, _('User deleted successfully'), extra_tags='alert alert-success')            
            return redirect('/users')


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
