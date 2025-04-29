from django.db import models
from django.contrib.auth.models import AbstractUser, Group, PermissionsMixin
# from django.core.validators import RegexValidator                     
# from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
#from task_manager.tasks.models import Tasks

# Create your models here.


class Users(AbstractUser, PermissionsMixin):
    
#    id = models.BigIntegerField(primary_key=True, auto_created=True)
    first_name = models.TextField(max_length=150, verbose_name=_('Name'))
    last_name = models.TextField(max_length=150, verbose_name=_('Surname'))
    username = models.TextField(
        max_length=150,
        unique=True,
        verbose_name=_('Username'),
#        validators=[
#            RegexValidator(
#                regex=r'^[A-Z]{3}\d{3}$',
#                message="Enter a valid registration number in the format ABC123.",
#                code="invalid_registration",
#                ),
#            ],
        )
#    executor = models.ForeignKey(Tasks, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Executor")
    password = models.TextField(max_length=20, verbose_name=_('Password'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation date'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date'))
 
    USERNAME_FIELD = 'username'

#    group = Group.objects.create(name='Users')
#    user = Users.objects.get(username=username)
#    user.groups.add(group)

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
