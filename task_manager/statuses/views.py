from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.utils.translation import gettext_lazy as _
from task_manager.statuses.forms import CreateStatusForm
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.constants import ERROR_MESSAGE, ERROR_URL


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/statuses.html'

    def handle_no_permission(self):
        messages.error(self.request, ERROR_MESSAGE)
        return redirect(ERROR_URL)


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = CreateStatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses:statuses')
    success_message = _('Status created successfully!')

    def handle_no_permission(self):
        messages.error(self.request, ERROR_MESSAGE)
        return redirect(ERROR_URL)


class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    success_url = reverse_lazy('statuses:statuses')
    template_name = 'statuses/delete.html'
    success_message = _('Status deleted successfully!')

    def form_valid(self, form):
        if Task.objects.filter(status=self.object):
            messages.error(
                self.request,
                _("It is not possible to delete a status because it is in use")
            )
            return redirect(self.success_url)
        super().form_valid(form)
        return redirect(self.success_url)

    def handle_no_permission(self):
        messages.error(self.request, ERROR_MESSAGE)
        return redirect(ERROR_URL)


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = CreateStatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses:statuses')
    success_message = _('Status updated successfully!')

    def handle_no_permission(self):
        messages.error(self.request, ERROR_MESSAGE)
        return redirect(ERROR_URL)
