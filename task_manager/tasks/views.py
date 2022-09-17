from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView
from django.utils.translation import gettext_lazy as _
from django_filters.views import FilterView
from task_manager.statuses.utils import LoginUserCheckingMixin
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import CreateTaskForm
from task_manager.tasks.models import Task


SUCCESS_URL = reverse_lazy('tasks:tasks')


class TaskListView(LoginUserCheckingMixin, FilterView):
    model = Task
    template_name = 'tasks/tasks.html'
    filterset_class = TaskFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_text'] = _('Show')
        context['filter'] = TaskFilter(self.request.GET, queryset=self.get_queryset())
        return context


class TaskCreateView(LoginUserCheckingMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = CreateTaskForm
    template_name = 'form.html'
    success_url = SUCCESS_URL
    success_message = _('Task created successfully!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Create task')
        context['button_text'] = _('Create')
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskDetailView(LoginUserCheckingMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'


class TaskDeleteView(
    LoginUserCheckingMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    DeleteView
):
    model = Task
    success_url = SUCCESS_URL
    template_name = 'delete.html'
    success_message = _('Task deleted successfully!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Deleting task')
        context['button_text'] = _('Yes, delete')
        return context

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(
            self.request,
            _('Task can be deleted only by its author.')
        )
        return redirect(self.success_url)


class TaskUpdateView(LoginUserCheckingMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = CreateTaskForm
    template_name = 'form.html'
    success_url = SUCCESS_URL
    success_message = _('Task updated successfully!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Updating task')
        context['button_text'] = _('Update')
        return context
