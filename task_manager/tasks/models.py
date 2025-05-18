from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Labels
from task_manager.statuses.models import Statuses
from task_manager.users.models import Users


class Tasks(models.Model):
    
    name = models.TextField(max_length=150, verbose_name=_('Name'))
    author = models.TextField(max_length=150, blank=True, null=True, verbose_name=_('Author'))
    discription = models.TextField('discription', max_length=100)
    status = models.ForeignKey(Statuses, on_delete=models.PROTECT, blank=True, null=True, verbose_name=_("Status"))
    executor = models.ForeignKey(Users, on_delete=models.PROTECT, blank=True, null=True, verbose_name=_("Executor"))
    label = models.ManyToManyField(Labels, blank=True, verbose_name=_("Labels"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation date'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date'))

    def __str__(self):
        return self.name
