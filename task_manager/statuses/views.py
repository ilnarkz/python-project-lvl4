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


class StatusListView(LoginUserCheckingMixin, ListView):
    model = Status
    template_name = 'statuses/statuses.html'


class StatusCreateView(LoginUserCheckingMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = CreateStatusForm
    template_name = 'form.html'
    success_url = reverse_lazy('statuses:statuses')
    success_message = _('Status created successfully!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Create status')
        context['button_text'] = _('Create')
        return context


class StatusDeleteView(LoginUserCheckingMixin, SuccessMessageMixin, DeleteView):
    model = Status
    success_url = reverse_lazy('statuses:statuses')
    template_name = 'delete.html'
    success_message = _('Status deleted successfully!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Delete status')
        return context

    def form_valid(self, form):
        if Task.objects.filter(status=self.object):
            messages.error(self.request, _("Status can not be deleted because it is in use."))
            return redirect(self.success_url)
        self.object.delete()
        return redirect(self.success_url)


class StatusUpdateView(LoginUserCheckingMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = CreateStatusForm
    template_name = 'form.html'
    success_url = reverse_lazy('statuses:statuses')
    success_message = _('Status updated successfully!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Update status')
        context['button_text'] = _('Update')
        return context
