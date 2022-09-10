from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    name = models.CharField(_('Name'), max_length=100, unique=True)
    created_at = models.DateTimeField(_('Created date'), default=timezone.now)

    def get_absolute_url(self):
        return reverse('statuses:statuses')

    def __str__(self):
        return self.name
