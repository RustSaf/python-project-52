from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
# from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Users(AbstractUser, PermissionsMixin):
    
    first_name = models.TextField(max_length=150, verbose_name=_('Name'))
    last_name = models.TextField(max_length=150, verbose_name=_('Surname'))
    username = models.TextField(max_length=150, unique=True, verbose_name=_('Username'))
    password = models.TextField(max_length=20, verbose_name=_('Password'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation date'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date'))
 
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

#     name = models.CharField(max_length=200) # название статьи
#     body = models.TextField() # тело статьи
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return self.name


# class ArticleComment(models.Model):
#     content = models.CharField('comment', max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
#    article = models.ForeignKey(Article, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Статьи")
