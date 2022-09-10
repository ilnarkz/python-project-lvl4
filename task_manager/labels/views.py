from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.utils.translation import gettext_lazy as _
from task_manager.labels.forms import CreateLabelForm
from task_manager.labels.models import Label
from task_manager.statuses.utils import LoginUserCheckingMixin
from task_manager.tasks.models import Task


class LabelListView(LoginUserCheckingMixin, ListView):
    model = Label
    template_name = 'labels/labels.html'
    success_url = reverse_lazy('labels:labels')
    error_url = reverse_lazy('login')


class LabelCreateView(LoginUserCheckingMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = CreateLabelForm
    template_name = 'form.html'
    success_url = reverse_lazy('labels:labels')
    success_message = _('Label created successfully!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Create label')
        context['button_text'] = _('Create')
        return context


class LabelDeleteView(LoginUserCheckingMixin, SuccessMessageMixin, DeleteView):
    model = Label
    success_url = reverse_lazy('labels:labels')
    template_name = 'delete.html'
    success_message = _('Label deleted successfully!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Delete label')
        return context

    def form_valid(self, form):
        if Task.objects.filter(labels=self.object):
            messages.error(self.request, _("Label can not be deleted because it is in use."))
            return redirect(self.success_url)
        self.object.delete()
        return redirect(self.success_url)


class LabelUpdateView(LoginUserCheckingMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = CreateLabelForm
    template_name = 'form.html'
    success_url = reverse_lazy('labels:labels')
    success_message = _('Label updated successfully!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Update label')
        context['button_text'] = _('Update')
        return context
