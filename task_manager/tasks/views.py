from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView
from django.utils.translation import gettext_lazy as _
from django_filters.views import FilterView
from task_manager.constants import ERROR_MESSAGE, ERROR_URL
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import CreateTaskForm
from task_manager.tasks.models import Task


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/tasks.html'
    filterset_class = TaskFilter

    def handle_no_permission(self):
        messages.error(self.request, ERROR_MESSAGE)
        return redirect(ERROR_URL)


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = CreateTaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:tasks')
    success_message = _('Task created successfully!')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(self.request, ERROR_MESSAGE)
        return redirect(ERROR_URL)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'


class TaskDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    DeleteView
):
    model = Task
    success_url = reverse_lazy('tasks:tasks')
    template_name = 'tasks/delete.html'
    success_message = _('Task deleted successfully!')

    def test_func(self):
        return self.get_object().author == self.request.user and not self.request.user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request, ERROR_MESSAGE)
            return redirect(ERROR_URL)
        messages.error(self.request, _("Task can be deleted only by its author."))
        return redirect(self.success_url)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = CreateTaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks:tasks')
    success_message = _('Task updated successfully!')

    def handle_no_permission(self):
        messages.error(self.request, ERROR_MESSAGE)
        return redirect(ERROR_URL)
