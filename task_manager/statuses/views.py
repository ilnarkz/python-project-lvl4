from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.utils.translation import gettext_lazy as _
from task_manager.statuses.forms import CreateStatusForm
from task_manager.statuses.models import Status
from task_manager.statuses.utils import LoginUserCheckingMixin
from task_manager.tasks.models import Task


SUCCESS_URL = reverse_lazy('statuses:statuses')


class StatusListView(LoginUserCheckingMixin, ListView):
    model = Status
    template_name = 'statuses/statuses.html'


class StatusCreateView(LoginUserCheckingMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = CreateStatusForm
    template_name = 'form.html'
    success_url = SUCCESS_URL
    success_message = _('Status created successfully!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Create status')
        context['button_text'] = _('Create')
        return context


class StatusDeleteView(LoginUserCheckingMixin, SuccessMessageMixin, DeleteView):
    model = Status
    success_url = SUCCESS_URL
    template_name = 'delete.html'
    success_message = _('Status deleted successfully!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Deleting status')
        context['button_text'] = _('Yes, delete')
        return context

    def form_valid(self, form):
        if Task.objects.filter(status=self.object):
            messages.error(self.request, _("It is not possible to delete a status because it is in use"))
            return redirect(self.success_url)
        self.object.delete()
        return redirect(self.success_url)


class StatusUpdateView(LoginUserCheckingMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = CreateStatusForm
    template_name = 'form.html'
    success_url = SUCCESS_URL
    success_message = _('Status updated successfully!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Updating status')
        context['button_text'] = _('Update')
        return context
