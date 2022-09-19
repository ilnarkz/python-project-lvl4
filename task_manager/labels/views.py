from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.utils.translation import gettext_lazy as _
from task_manager.labels.forms import CreateLabelForm
from task_manager.labels.models import Label
from task_manager.constants import ERROR_MESSAGE, ERROR_URL
from task_manager.tasks.models import Task


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/labels.html'

    def handle_no_permission(self):
        messages.error(self.request, ERROR_MESSAGE)
        return redirect(ERROR_URL)


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = CreateLabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels:labels')
    success_message = _('Label created successfully!')

    def handle_no_permission(self):
        messages.error(self.request, ERROR_MESSAGE)
        return redirect(ERROR_URL)


class LabelDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    success_url = reverse_lazy('labels:labels')
    template_name = 'labels/delete.html'
    success_message = _('Label deleted successfully!')

    def form_valid(self, form):
        if Task.objects.filter(labels=self.object):
            messages.error(
                self.request,
                _("It is not possible to delete a label because it is in use")
            )
            return redirect(self.success_url)
        super().form_valid(form)
        return redirect(self.success_url)

    def handle_no_permission(self):
        messages.error(self.request, ERROR_MESSAGE)
        return redirect(ERROR_URL)


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = CreateLabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels:labels')
    success_message = _('Label updated successfully!')

    def handle_no_permission(self):
        messages.error(self.request, ERROR_MESSAGE)
        return redirect(ERROR_URL)
