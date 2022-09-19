from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'), null=True)
    status = models.ForeignKey(
        Status,
        related_name='statuses',
        on_delete=models.PROTECT,
        verbose_name=_('Status'),
        null=False
    )
    labels = models.ManyToManyField(Label, verbose_name=_('Labels'), blank=True)
    author = models.ForeignKey(
        User,
        related_name='authors',
        verbose_name=_('Author'),
        on_delete=models.PROTECT
    )
    executor = models.ForeignKey(
        User,
        related_name='executors',
        on_delete=models.PROTECT,
        verbose_name=_('Executor'),
        blank=True,
        null=False
    )
    created_at = models.DateTimeField(_('Created date'), default=timezone.now)

    def get_absolute_url(self):
        return reverse('tasks:tasks')

    def __str__(self):
        return self.name
