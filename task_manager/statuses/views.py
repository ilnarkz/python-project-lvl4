from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.utils.translation import gettext_lazy as _
from task_manager.statuses.forms import CreateStatusForm
from task_manager.statuses.models import Status
from task_manager.statuses.utils import LoginUserCheckingMixin


class StatusListView(LoginUserCheckingMixin, ListView):
    model = Status
    template_name = 'statuses/statuses.html'
    success_url = reverse_lazy('statuses:statuses')
    error_url = reverse_lazy('login')


class StatusCreateView(LoginUserCheckingMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = CreateStatusForm
    template_name = 'form.html'
    success_url = reverse_lazy('statuses:statuses')
    success_message = _('Status created successfully!')
    error_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Create status')
        context['button_text'] = _('Create')
        return context


class StatusDeleteView(LoginUserCheckingMixin, SuccessMessageMixin, DeleteView):
    model = Status
    success_url = reverse_lazy('statuses:statuses')
    template_name = 'delete.html'
    error_url = reverse_lazy('login')
    success_message = _('Status deleted successfully!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Delete status')
        return context


class StatusUpdateView(LoginUserCheckingMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = CreateStatusForm
    template_name = 'form.html'
    success_url = reverse_lazy('statuses:statuses')
    error_url = reverse_lazy('login')
    success_message = _('Status updated successfully!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Update status')
        context['button_text'] = _('Update')
        return context
