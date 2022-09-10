from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), null=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name=_('status'), null=False)
    labels = models.ManyToManyField(Label)
    author = models.ForeignKey(User, related_name='task_author', verbose_name=_('author'), on_delete=models.PROTECT)
    performer = models.ForeignKey(User, related_name='task_performer', on_delete=models.PROTECT, verbose_name=_('performer'), null=False)
    created_at = models.DateTimeField(_('created date'), default=timezone.now)

    def get_absolute_url(self):
        return reverse('tasks:tasks')

    def __str__(self):
        return self.name
