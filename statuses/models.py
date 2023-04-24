from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Statuses(models.Model):
    name = models.CharField(_('name'), max_length=255, unique=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    # task_id = models.ForeignKey('Task', null=True, blank=True,
    #                             on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return self.name
