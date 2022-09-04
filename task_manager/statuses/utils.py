from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class LoginUserCheckingMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, _('You are not logged in! Please, log in. '))
            return redirect(self.error_url)
        return super().dispatch(request, *args, **kwargs)
