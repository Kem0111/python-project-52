from django.db import models
from django.utils.translation import gettext_lazy as _


class Labels(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _('Labels')
        verbose_name_plural = _('Labels')
        ordering = ['-created_at']
