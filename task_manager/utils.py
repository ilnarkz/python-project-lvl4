from django.contrib import messages
from django.shortcuts import redirect
from task_manager.constants import ERROR_MESSAGE, ERROR_URL


class NoPermissionMixin:

    def handle_no_permission(self):
        messages.error(self.request, ERROR_MESSAGE)
        return redirect(ERROR_URL)
