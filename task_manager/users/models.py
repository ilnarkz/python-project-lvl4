from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    @staticmethod
    def get_absolute_url():
        return reverse('users')

    def __str__(self):
        return self.get_username()
