from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Users(AbstractUser, PermissionsMixin):

    first_name = models.TextField(
        max_length=150,
        verbose_name=_('Name')
        )
    last_name = models.TextField(
        max_length=150,
        verbose_name=_('Surname')
        )
    username = models.TextField(
        max_length=150,
        unique=True,
        verbose_name=_('Username'),
        )
    password = models.TextField(
        max_length=20,
        verbose_name=_('Password')
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Creation date')
        )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Update date')
        )
 
    USERNAME_FIELD = 'username'

    def get_absolute_url_update(self):
        return reverse('users:user_update', args=[str(self.id)])
    
    def get_absolute_url_delete(self):
        return reverse('users:user_delete', args=[str(self.id)])

    def __str__(self):
        return self.username
