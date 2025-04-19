from django.db import models
from django.utils.translation import gettext_lazy as _
#from task_manager.tasks.models import Tasks
# Create your models here.

# id
# Name
# Дата создания/ и модификации

class Labels(models.Model):
    
    name = models.TextField(max_length=150, verbose_name=_('Name'))
#    task = models.ManyToManyField(Tasks, blank=True, null=True, verbose_name="Labels")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation date'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date'))

    def __str__(self):
        return self.name