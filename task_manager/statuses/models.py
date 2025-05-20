from django.db import models
from django.utils.translation import gettext_lazy as _


class Statuses(models.Model):
    
    name = models.TextField(max_length=150, verbose_name=_('Name'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Creation date')
        )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_('Update date')
        )

    def __str__(self):
        return self.name