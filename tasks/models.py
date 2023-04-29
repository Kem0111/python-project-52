from django.db import models
from django.utils.translation import gettext_lazy as _
from statuses.models import Statuses
from django.contrib.auth.models import User
from labels.models import Labels


class Tasks(models.Model):
    name = models.CharField(_('name'), max_length=255, unique=True)
    status = models.ForeignKey(
        Statuses,
        on_delete=models.PROTECT,
        null=False,
        verbose_name=_('status')
    )
    description = models.TextField(_('description'), blank=True, null=True)
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=False,
        related_name='author_tasks',
        verbose_name=_('author')
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        related_name='executor_tasks',
        verbose_name=_('executor')
    )
    labels = models.ManyToManyField(
        Labels,
        blank=True,
        verbose_name=_('Labels')
    )
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _('Tasks')
        verbose_name_plural = _('Tasks')
        ordering = ['-created_at']
