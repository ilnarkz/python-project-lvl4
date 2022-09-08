from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class LoginUserCheckingMixin:
    error_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _('You are not logged in! Please, log in. '))
            return redirect(self.error_url)
        return super().dispatch(request, *args, **kwargs)
