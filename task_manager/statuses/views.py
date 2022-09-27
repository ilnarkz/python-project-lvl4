from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.utils.translation import gettext_lazy as _
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.utils import NoPermissionMixin


class StatusListView(NoPermissionMixin, LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/statuses.html'


class StatusCreateView(NoPermissionMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses:statuses')
    success_message = _('Status created successfully!')


class StatusDeleteView(NoPermissionMixin, LoginRequiredMixin, SuccessMessageMixin, DeleteView):
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
        return super().form_valid(form)


class StatusUpdateView(NoPermissionMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses:statuses')
    success_message = _('Status updated successfully!')
