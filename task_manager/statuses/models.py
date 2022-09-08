from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    name = models.CharField(_('name'), max_length=100)
    created_at = models.DateTimeField(_('created date'), default=timezone.now)

    def get_absolute_url(self):
        return reverse('statuses:statuses')

    def __str__(self):
        return self.name
